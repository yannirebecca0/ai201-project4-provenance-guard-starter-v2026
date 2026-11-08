# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A client submits a text payload along with a `creator_id` to the `/submit` endpoint. The service validates the input data, generates a unique UUID `content_id`, and feeds the text into two independent evaluation signals: a local transformer model (`detector.py`) and a stylometric analyzer (`stylometry.py`). The resulting scores are combined using a weighted rule in `scoring.combine_signals(...)`, which maps to a final confidence score and a plain-English label variant. The system writes a complete audit record containing both signal scores, the confidence, the guess, and the label to `logs/audit.jsonl`, and returns the structured JSON response to the client. If a writer disputes the decision, they can invoke the `/appeal` endpoint with their `content_id` and reasoning, which verifies the log entry, appends the appeal event, and transitions the submission status to `under_review`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a local transformer model (`gpt2`): its perplexity, squashed onto 0–1 in `detector.py::model_signal` so that low perplexity (very predictable text) scores close to 1.

**Why that might differ between human and AI writing:** Machine-generated text tends to exhibit highly predictable token trajectories and smoother conditional probabilities compared to spontaneous human writing.

**What it can't see:** It cannot evaluate broader narrative context, factual accuracy, or deep authorial intent, and can be tripped up by heavily stylized human prose or formal academic writing.

### Signal two — the style signal

**What it measures:** Surface-level textual attributes in `stylometry.py::style_signal`: sentence length spread (standard deviation over mean), lexical diversity (unique-to-total word ratio over 50-word windows), and punctuation density (commas, semicolons, dashes and similar marks per word). Each is flipped so higher means more AI-like, then combined with weights 0.4 / 0.35 / 0.25.

**Why that might differ between human and AI writing:** Human writing often contains irregular sentence variations, higher lexical richness, and organic punctuation rhythm compared to uniform AI generation patterns.

**What it can't see:** It completely lacks semantic understanding; it treats words purely as mathematical tokens, meaning a sophisticated machine-generated essay with randomized vocabulary can easily bypass its style checks.

### The combining rule

**The rule:** A weighted average of the model score and the style score. The protection for human writers comes from the label thresholds: only scores above 0.70 are called AI, which leaves a wide "unsure" band (0.36–0.70) for borderline text.

**The numbers:** Model score weighted at 0.6 and stylometry score weighted at 0.4.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:** 
When an AI-generated text has been heavily edited or injected with varied vocabulary, the style signal might score it as very human (low score), while the deep semantic model still flags artificial probability patterns (high score). The combining rule balances these via weighted averaging to prevent a single noisy surface metric from overriding deep semantic signals.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 - 0.35 | We are confident this piece was written by a human writer. |
| unsure | 0.36 - 0.70 | We are uncertain about the authorship of this text; it contains mixed signals. |
| high-confidence AI | 0.71 - 1.00 | We are confident this text was generated by artificial intelligence. |

**Why I worded the "unsure" one this way:**
It avoids making any definitive accusations of cheating. Because the reader or submitter may have written every word themselves, framing it around "mixed signals" and institutional uncertainty prevents unnecessary panic and preserves trust while keeping the door open for human review.

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I burned the toast again. Third time this week — my roommate says I should just buy a new toaster, but honestly? The old one has character. It hums. It pops whenever it feels like it, sometimes twice. Anyway, breakfast was cereal.", "creator_id": "writer_1"}'

{
  "confidence": 0.2099,
  "content_id": "a8ee30a9-4050-4a90-a95d-4c2f15497934",
  "guess": "human",
  "label": "We are confident this piece was written by a human writer.",
  "model_score": 0.2849,
  "style_score": 0.0975
}
```

**An appeal**

```bash
curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "a8ee30a9-4050-4a90-a95d-4c2f15497934", "reasoning": "I wrote this myself about my own kitchen this morning."}'

{
  "content_id": "a8ee30a9-4050-4a90-a95d-4c2f15497934",
  "message": "Appeal recorded successfully. Your submission is under review.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
curl "http://127.0.0.1:5000/log?limit=2"

{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.2099,
      "confidence": 0.2099,
      "content_id": "a8ee30a9-4050-4a90-a95d-4c2f15497934",
      "creator_id": "writer_1",
      "guess": "human",
      "label": "We are confident this piece was written by a human writer.",
      "model_score": 0.2849,
      "status": "submitted",
      "style_score": 0.0975,
      "timestamp": "2026-11-02T04:17:02+00:00"
    },
    {
      "content_id": "a8ee30a9-4050-4a90-a95d-4c2f15497934",
      "creator_id": "writer_1",
      "event": "appeal",
      "reasoning": "I wrote this myself about my own kitchen this morning.",
      "status": "under_review",
      "timestamp": "2026-11-02T04:17:02+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Guidance on structuring the Flask route in app.py to gracefully reject malformed JSON payloads and empty text inputs with a 400 error
- *What came back:* An example validation block checking request.get_json(silent=True) and returning JSON error responses before hitting model inference
- *What I changed:* Integrated the type and length checks directly into the /submit endpoint to satisfy Acceptance Criterion #5

**Moment 2**

- *What I asked for:* Help debugging a TypeError in app.py when calling audit.log_appeal inside the /appeal route
- *What came back:* An explanation that log_appeal required the creator_id argument, which could be retrieved by querying existing audit entries for that content_id
- *What I changed:* Updated the appeal() handler to fetch the original creator_id from audit.entries_for(content_id) before calling audit.log_appeal

**Moment 3**

- *What I asked for:* Help getting the unit 7 submission ready, after finding `stylometry.py` and `scoring.py` were still the starter stubs
- *What came back:* Claude (Claude Code) wrote the three style measures and `style_signal` in `stylometry.py`, the weighted-average rule and label mapping in `scoring.py`, and set the 0.6 / 0.4 weights and 0.35 / 0.70 thresholds in `config.py` to match the rule I had described in this README
- *What I changed:* Checked the scores on human, AI and plain-writing samples before keeping it, and re-ran the sample submission and appeal with the finished code

**Moment 4**

- *What I asked for:* Help with unit 8 Milestone 1: turning on rate limiting and logging refused requests
- *What came back:* Claude turned the limiter on at 5 per minute / 50 per day and added a `_reject` helper in `app.py` so every 400 and 404 is written to the audit log with `audit.log_rejection`
- *What I changed:* Ran the flood test and checked the log entries for the 429s and 400s myself

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
A real writer submits their own work a few times an hour at most, and even someone re-checking a draft after small edits rarely sends more than one or two a minute, so 5 a minute and 50 a day never gets in their way. A script trying to map my thresholds needs hundreds or thousands of near-identical variations; at 5 a minute it would take hours to send even a few hundred, and 50 a day caps any one caller well below what threshold-mapping needs.

**What a caller counts as:** Per `creator_id`, falling back to the caller's address when a request has no usable `creator_id` (`app.py::rate_limit_key`). The weakness is that `creator_id` is whatever the caller types, so one script can rotate through a thousand made-up IDs and look like a thousand writers. Keying on address instead would catch that script, but it would also lump together everyone behind one shared network (a household, a school), so they would share one limit.

<!-- python run_attacks.py --flood 15 -->

**The run of status codes when I pushed past it:** (`results/flood_2026-11-08_1421.md`, 15 submissions as `flood_tester`)

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

Every one of the ten 429s was written to `logs/audit.jsonl` as a `rejected` entry with `"reason": "rate_limited"` and `"limit": "5 per 1 minute"`.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
