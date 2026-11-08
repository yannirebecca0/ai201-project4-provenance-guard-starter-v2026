#!/usr/bin/env python3
"""
Criterion 4: every appeal with a valid content_id moves the item to
`under_review` and lands in the audit log.

run_eval.py only sends submissions, so this does the two-step version: submit,
take the content_id that comes back, appeal it, then read the log to check the
appeal was recorded. Five per trial, three trials.

    python run_appeals.py --label before
"""

import argparse
import datetime as dt
import json

import requests

import config

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

TEXT = (
    "We got to the campsite about four. The pitch was fine, a bit sloped, but "
    "there was a tap nearby. Putting the tent up took longer than it should have. "
    "Then it rained hard and kept raining, so we played cards in the tent."
)


def one_appeal(url, creator_id):
    """Submit, appeal, then check the log. Returns what happened at each step."""
    sub = requests.post(f"{url}/submit", json={"text": TEXT, "creator_id": creator_id},
                        timeout=90)
    result = {"creator_id": creator_id, "submit_status": sub.status_code}
    content_id = sub.json().get("content_id") if sub.ok else None
    result["content_id"] = content_id
    if not content_id:
        result["passed"] = False
        return result

    app = requests.post(f"{url}/appeal", timeout=30, json={
        "content_id": content_id,
        "reasoning": "I wrote this myself.",
    })
    body = app.json() if app.content else {}
    result["appeal_status"] = app.status_code
    result["returned_status"] = body.get("status")

    entries = requests.get(f"{url}/log", params={"limit": 50}, timeout=10).json()["entries"]
    logged = [e for e in entries
              if e.get("content_id") == content_id and e.get("event") == "appeal"]
    result["appeal_in_log"] = bool(logged)

    result["passed"] = (app.status_code == 200
                        and body.get("status") == "under_review"
                        and bool(logged))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--per-trial", type=int, default=5)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    trials = []
    for trial in range(1, args.trials + 1):
        # A fresh creator_id per submission keeps the rate limiter out of it.
        results = [one_appeal(args.url, f"eval_appeal_{stamp}_t{trial}_{i}")
                   for i in range(1, args.per_trial + 1)]
        passed = sum(r["passed"] for r in results)
        print(f"  trial {trial}: {passed}/{len(results)}")
        trials.append(results)

    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeals_{stamp}{label}.md"
    config.RESULTS_DIR.mkdir(exist_ok=True)
    lines = [
        f"# Appeal path — criterion 4{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_appeals.py::main`",
        "- Service: `app.py::submit`, `app.py::appeal`, checked against `GET /log`",
        f"- {args.trials} trials of {args.per_trial} · "
        f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| Trial | Passed |",
        "|---|---|",
    ]
    lines += [f"| {i} | {sum(r['passed'] for r in t)}/{len(t)} |"
              for i, t in enumerate(trials, 1)]
    lines += [""]
    for i, t in enumerate(trials, 1):
        lines += [f"**Trial {i}**", "", "```json", json.dumps(t, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
