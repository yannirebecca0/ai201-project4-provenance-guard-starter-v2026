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

**Moment 5**

- *What I asked for:* Claude to run the attack set and write up Milestone 2
- *What came back:* Claude ran all 56 attacks, set the held/broke rule, marked each attack, picked the ten audit entries and chose MF07 as the worst outcome
- *What I changed:* Nothing yet. The marks follow the rule written at the top of Attack Run — Before

**Moment 6**

- *What I asked for:* Help building `scenarios.py` for my five criteria
- *What came back:* My first draft of criterion 1 used AI-generated paragraphs in place of my own writing. Claude pointed out that this would make the false-positive test meaningless, so I replaced them with ten real text messages I had sent. Claude wrote the five "clearly AI" paragraphs for criterion 2, the bad-input bodies, and `run_appeals.py` for criterion 4, then ran all three trials
- *What I changed:* Supplied my own messages for criterion 1

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

Full run: `results/attack_run_2026-11-08_1424_before.md` (56 attacks, `run_attacks.py --set attack_set --label before`). Nothing crashed: no 5xx on any input.

**How I marked them.** An attack BROKE if it got the outcome it was going for at high confidence. "Unsure" counts as HELD, because that band exists to send borderline text to a human instead of accusing anyone.

- **Evasion** (AI text trying to pass): broke if labelled *human*.
- **False positive** (real human writing): broke if labelled *AI*.
- **Prompt injection:** broke if labelled *human*, or if it changed the label text or the audit log.
- **Malformed text:** broke if the service crashed **or** gave a confident verdict on something that isn't scorable writing; it should have been refused.
- **Malformed requests and flood:** broke on a crash or on getting past validation or the limit.

Under a stricter reading where "unsure" also counts as a miss for evasion, 9 of 10 evasion attacks broke instead of 3.

| Family | Attacks | Broke | Held |
|---|---|---|---|
| evasion | 10 | 3 | 7 |
| false_positive | 8 | 3 | 5 |
| prompt_injection | 6 | 1 | 5 |
| malformed (text) | 8 | 5 | 3 |
| malformed (requests) | 12 | 0 | 12 |
| flood_same_creator | 12 | 0 | 12 |
| **Total** | **56** | **12** | **44** |

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `e5afc06a-7580-4849-bd1a-970d8f7f89f0` | human | 0.298 || BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `53c59147-6a9b-4351-b7be-cdb1538d9568` | unsure | 0.435 || HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `336f5741-e566-459a-ac12-b1a6a4907ee1` | unsure | 0.521 || HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `5a1a6bbc-4e7e-4a3b-a37a-103a7cefb1c2` | unsure | 0.558 || HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `62ff24ec-3ebc-4146-80fb-15a9f0d82133` | human | 0.256 || BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `7b5fe033-2525-4c0d-962d-d0b62e324565` | unsure | 0.428 || HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `2d31340f-0697-4709-8eb6-1c2ddbf67f66` | unsure | 0.434 || HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `87f16c98-d3f3-4615-b9b1-f8aa15e3edb1` | human | 0.343 || BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `981af843-7bc8-4915-8ff9-1f4fab6941d7` | unsure | 0.549 || HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `1d9fccc1-30df-46ce-877f-d0716b90ceb2` | ai | 0.897 || HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f39b10e1-16eb-4432-a7e4-c745a6a20cd0` | unsure | 0.541 || HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `a60ced4b-e74d-4822-8ca0-65e343a53047` | unsure | 0.687 || HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `a1de7adf-d47f-4db5-b73b-699867c02cd1` | unsure | 0.685 || HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `673162dc-40be-4605-bb16-319df16b24e3` | unsure | 0.685 || HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `0f304578-15c3-40ad-a117-4f2861965cc8` | ai | 0.788 || BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `dae8ea8a-f3cc-40ce-9f81-6c0fc76115a7` | ai | 0.715 || BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `56a23f09-742f-4b20-afc0-a0ea431bdf1c` | ai | 0.752 || BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `417f1baf-f6fc-4a7c-93f7-3fbdd5b8f502` | unsure | 0.354 || HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `9af55782-23e3-4963-a69b-bf3b8320cefe` | unsure | 0.386 || HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f59fa22a-6515-4737-b0a0-1fbf52097b39` | human | 0.211 || BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `7d57fb45-71a5-47d0-9743-b824575c7f10` | unsure | 0.511 || HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `9d749de1-56df-4b74-9a74-05498a56cfb8` | unsure | 0.430 || HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f39ea65e-ed5a-460c-86b0-05b919eb9f3c` | unsure | 0.436 || HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `50475750-36fb-4bc8-8d56-f34c7b571814` | unsure | 0.505 || HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — || HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — || HELD |
| MF03 | malformed | text is control characters | 200 | `b59d2a01-7580-42ae-8423-bae04da66f0f` | human | 0.180 || BROKE |
| MF04 | malformed | text is only punctuation | 200 | `c78beb23-e67f-4b76-aa27-98640b0865b9` | human | 0.207 || BROKE |
| MF05 | malformed | text is a very long single word | 200 | `2033a607-239f-4904-80bb-1136ed9fa05e` | ai | 0.779 || BROKE |
| MF06 | malformed | text is emoji only | 200 | `a44f3e25-6763-4488-beaa-244ac54def5c` | ai | 0.798 || BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `d1b79447-7d68-43c1-97e4-4a536486ab64` | ai | 0.744 || BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — || HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — || HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — || HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — || HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — || HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — || HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — || HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — || HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — || HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — || HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — || HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — || HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — || HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3c5f2e34-74bd-4c9f-8fda-1085e441d3d7` | human | 0.197 || HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `45fa5676-105c-48f5-bc13-2e5b6fe940de` | human | 0.197 || HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5d5ad422-d497-4266-88f5-3b7e641280de` | human | 0.197 || HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `30d4073d-8910-42a6-91a4-5bacec8b609e` | human | 0.197 || HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9039919e-baad-4922-b9d3-16d1749bea34` | human | 0.197 || HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From `logs/audit.jsonl`. Real writing called AI (FP07, FP05), non-English and non-text called AI (MF07, MF06), junk called human (MF03), AI text that passed as human (EV01, EV05, PI02), and two rejections: a 400 from my route and a 429 from the limiter.

```json
{"timestamp": "2026-11-08T19:24:10+00:00", "content_id": "56a23f09-742f-4b20-afc0-a0ea431bdf1c", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.5576, "combined_score": 0.752, "label": "We are confident this text was generated by artificial intelligence.", "status": "submitted", "confidence": 0.752}
{"timestamp": "2026-11-08T19:24:10+00:00", "content_id": "0f304578-15c3-40ad-a117-4f2861965cc8", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.77, "combined_score": 0.7883, "label": "We are confident this text was generated by artificial intelligence.", "status": "submitted", "confidence": 0.7883}
{"timestamp": "2026-11-08T19:24:11+00:00", "content_id": "d1b79447-7d68-43c1-97e4-4a536486ab64", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 0.5, "combined_score": 0.7438, "label": "We are confident this text was generated by artificial intelligence.", "status": "submitted", "confidence": 0.7438}
{"timestamp": "2026-11-08T19:24:11+00:00", "content_id": "a44f3e25-6763-4488-beaa-244ac54def5c", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 0.5, "combined_score": 0.7981, "label": "We are confident this text was generated by artificial intelligence.", "status": "submitted", "confidence": 0.7981}
{"timestamp": "2026-11-08T19:24:11+00:00", "content_id": "b59d2a01-7580-42ae-8423-bae04da66f0f", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.45, "combined_score": 0.18, "label": "We are confident this piece was written by a human writer.", "status": "submitted", "confidence": 0.18}
{"timestamp": "2026-11-08T19:24:09+00:00", "content_id": "e5afc06a-7580-4849-bd1a-970d8f7f89f0", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.4993, "combined_score": 0.2978, "label": "We are confident this piece was written by a human writer.", "status": "submitted", "confidence": 0.2978}
{"timestamp": "2026-11-08T19:24:09+00:00", "content_id": "62ff24ec-3ebc-4146-80fb-15a9f0d82133", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.1574, "combined_score": 0.2557, "label": "We are confident this piece was written by a human writer.", "status": "submitted", "confidence": 0.2557}
{"timestamp": "2026-11-08T19:24:10+00:00", "content_id": "f59fa22a-6515-4737-b0a0-1fbf52097b39", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.222, "combined_score": 0.2114, "label": "We are confident this piece was written by a human writer.", "status": "submitted", "confidence": 0.2114}
{"timestamp": "2026-11-08T19:24:11+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "bad_request", "route": "/submit", "status_code": 400, "message": "Text exceeds maximum allowed length of 10,000 words."}
{"timestamp": "2026-11-08T19:24:11+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

PI04 (`<script>` in the text) and PI05 (fake JSON fields in the text) both HELD. The label text came back unchanged, and PI05's log line is still one well-formed JSON object, because `audit.py` writes with `json.dumps`, so the injected quotes are escaped instead of becoming fields.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**MF07**, a sentence of ordinary Arabic, came back *"We are confident this text was generated by artificial intelligence."* (combined 0.744, model 0.906). Nothing about it is AI. The system just can't read Arabic, and instead of saying so it accused the writer with full confidence. Emoji (MF06) failed the same way, which suggests this isn't one unlucky submission: writers in other non-Latin scripts may well get the same accusation. I only tested one Arabic input, so that's a suspicion, not a result.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Criteria 1, 2, 3 and 5: `results/run_2026-11-08_1511_before.md` (`run_eval.py --label before`, scenarios in `scenarios.py`). Criterion 4 can't be sent as text alone, so it ran from `run_appeals.py --label before` → `results/appeals_2026-11-08_1511_before.md`, which submits, appeals the returned `content_id`, then checks `GET /log` for the appeal entry.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. Gap between AI and human average scores | ≥ 0.40 | 0.450 | 0.450 | 0.450 | MET |
| 3. All three labels reachable | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Valid appeals reach `under_review` and the log | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input returns 400, not 500 | 6 of 6 | 6/6 | 6/6 | 6/6 | MET |

All three trials came out identical, down to the fourth decimal. That's expected: GPT-2 scoring runs without sampling and the style signal is plain arithmetic, so the same text gets the same score every time.

**How each verdict was reached**

1. My 10 texts were real messages I sent. 8 came back human and 2 unsure ("Can you please stop at ShopRite…" 0.356, and the long message to my dad 0.456). None were labelled AI.
2. Mean combined score for 5 Claude-generated paragraphs was 0.693; for my 10 messages it was 0.243. The gap is 0.450, above 0.40 in all three runs.
3. An AI paragraph, a casual paragraph and a plain paragraph came back ai, human and unsure.
4. All 15 appeals returned 200 with `status: under_review` and appeared in the log as `event: appeal`.
5. Empty, missing, 15,000-word, null, numeric and whitespace-only text all came back 400.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Criterion 1: trial 1, first three of ten, from `run_eval.py::main` → `app.py::submit`:

```json
[
  {
    "sent": "Can you please stop at ShopRite on the way home?",
    "guess": "unsure",
    "confidence": 0.3557,
    "model_score": 0.3762,
    "style_score": 0.325
  },
  {
    "sent": "Ok I’m very busy tmr but let’s buy these ticket",
    "guess": "human",
    "confidence": 0.1877,
    "model_score": 0.0128,
    "style_score": 0.45
  },
  {
    "sent": "Iced coffee with two cream and caramel with extra ice",
    "guess": "human",
    "confidence": 0.1966,
    "model_score": 0.0276,
    "style_score": 0.45
  }
]
```

Criterion 2: trial 1, the AI half, from `run_eval.py::main` → `app.py::submit` (the human half is criterion 1's output):

```json
[
  {
    "sent": "Artificial intelligence is transforming the way we live and work. It o",
    "guess": "ai",
    "confidence": 0.7461
  },
  {
    "sent": "Regular exercise is essential for maintaining good health. It helps st",
    "guess": "ai",
    "confidence": 0.7047
  },
  {
    "sent": "Time management is a crucial skill for students. By organizing tasks a",
    "guess": "unsure",
    "confidence": 0.6175
  },
  {
    "sent": "Climate change is one of the most pressing challenges facing the world",
    "guess": "ai",
    "confidence": 0.7719
  },
  {
    "sent": "Reading offers many benefits for people of all ages. It expands vocabu",
    "guess": "unsure",
    "confidence": 0.6261
  }
]
```

Criterion 3: trial 1, from `run_eval.py::main` → `app.py::submit`:

```json
[
  {
    "sent": "Artificial intelligence is transforming the way we live and work. It o",
    "status": 200,
    "guess": "ai",
    "confidence": 0.7461,
    "label": "We are confident this text was generated by artificial intelligence."
  },
  {
    "sent": "I burned the toast again. Third time this week — my roommate says I sh",
    "status": 200,
    "guess": "human",
    "confidence": 0.2099,
    "label": "We are confident this piece was written by a human writer."
  },
  {
    "sent": "I went to the store on Saturday. I bought milk, eggs and bread. The li",
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6908,
    "label": "We are uncertain about the authorship of this text; it contains mixed signals."
  }
]
```

Criterion 4: trial 1, from `run_appeals.py::one_appeal` → `app.py::submit`, `app.py::appeal`, `GET /log`:

```json
[
  {
    "creator_id": "eval_appeal_2026-11-08_1511_t1_1",
    "submit_status": 200,
    "content_id": "e60cccd8-07f5-4c3a-a73b-203e25a3150c",
    "appeal_status": 200,
    "returned_status": "under_review",
    "appeal_in_log": true,
    "passed": true
  },
  {
    "creator_id": "eval_appeal_2026-11-08_1511_t1_2",
    "submit_status": 200,
    "content_id": "232ddef7-96c8-4c57-8617-ecef21201822",
    "appeal_status": 200,
    "returned_status": "under_review",
    "appeal_in_log": true,
    "passed": true
  },
  {
    "creator_id": "eval_appeal_2026-11-08_1511_t1_3",
    "submit_status": 200,
    "content_id": "926b4994-4b37-41aa-80d0-c7fb33d7649b",
    "appeal_status": 200,
    "returned_status": "under_review",
    "appeal_in_log": true,
    "passed": true
  },
  {
    "creator_id": "eval_appeal_2026-11-08_1511_t1_4",
    "submit_status": 200,
    "content_id": "ac99d61f-85d2-4255-a8d4-de6331a4559c",
    "appeal_status": 200,
    "returned_status": "under_review",
    "appeal_in_log": true,
    "passed": true
  },
  {
    "creator_id": "eval_appeal_2026-11-08_1511_t1_5",
    "submit_status": 200,
    "content_id": "41a37e2c-8d1d-4f8e-ba22-2f17edede761",
    "appeal_status": 200,
    "returned_status": "under_review",
    "appeal_in_log": true,
    "passed": true
  }
]
```

Criterion 5: trial 1, from `run_eval.py::main` → `app.py::submit`:

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "word word word word word word word word word word word word word word "
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "   \n\t  "
  }
]
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

All five criteria were met, so every diagnosis below is for a broken attack. The 12 breaks fall into three patterns. For reference, the clean AI paragraph the evasion attacks are built from scores model 0.669 / style 0.499 / combined **0.601 (unsure)** before any attack is applied. My system doesn't confidently catch plain AI text even with no tricks.

**Pattern A: AI text labelled human (EV01, EV05, EV08, PI02)**

- **EV01 (typos). Stage: signal one.** The typos didn't fool the style signal: spread, word variety and punctuation are identical to the clean paragraph. But they dropped the model score from 0.669 to 0.164 (combined 0.601 → 0.298). Misspelled words break the token probability distributions: GPT-2 splits them into rare sub-word pieces it finds very surprising, so perplexity goes up and the model's AI score goes down.
- **PI02 (fake "SYSTEM:" message). Stages: signal one and signal two.** It wasn't the meaning of the instruction that lowered the score, since my model doesn't follow instructions. It was the fragmentation, short length and abrupt syntax breaks. Odd tokens like `SYSTEM:`, `guess=human, confidence=0.02` and the cut-off `Th` are surprising to GPT-2, so model score fell to 0.204. The short, choppy lines also raised sentence-length spread to 0.65, which my style signal reads as human (style 0.222).
- **EV05 (heavy human editing pass). Stages: signal two, and signal one.** The drastic drop in style score (0.157) was driven primarily by the spike in sentence-length spread from 0.16 to 0.68, as the human rewrite shattered the even, repetitive sentence rhythm of the original AI text. Word variety actually went down slightly (0.94 → 0.86), so it wasn't vocabulary. Given that a full human rewrite fundamentally changes authorship, this sample behaves more like authentic human text than corrupted AI output. It's marked BROKE by my rule, but it may be a "held" in disguise.
- **EV08 (two sentences, 10 words). Stage: signal one.** A perplexity score calculated on about 12 tokens is statistically unreliable, because a handful of words can disproportionately skew the probability distribution. With the style signal sitting near neutral (0.488), the model score (0.245) alone decided the final verdict.

**Were my targets too low?** Yes, in one place. All five criteria were met while the attack set broke 12 times, because criterion 1 only tested casual text messages. I would tighten criterion 1 by expanding the test set to include formal and professional prose (technical docs, cover letters, essays written to a rubric). My personal writing samples should cover the same register where the false positives actually happened in FP05–07.

**Pattern B: real human writing labelled AI (FP05, FP06, FP07; FP02 nearly, at 0.687)**

- **FP05 (technical docs), FP06 (cover letter). Stage: signal one, amplified by the combining rule.** Predictable, highly formulaic text uses standard vocabulary and rigid structural patterns that closely mimic the low-perplexity, uniform generation style of LLMs. Model scores were 0.800 and 0.881. FP05's style score (0.770) agreed, because its vocabulary repeats (word variety 0.63) and it has almost no punctuation.
- **FP07 (deliberate repetition). Stages: signal one and signal two, amplified by the combining rule.** Intentional repetition hurts word variety (type-token ratio 0.53), which pushes the style signal toward AI (0.558). Sentence-length spread stayed human-like at 0.73, so variety was the only style measure fooled. Meanwhile the 0.6 weight on the model amplified the false positive: predictable phrasing means low perplexity, and low perplexity is a high AI score (0.882).

**Pattern C: confident verdicts on things that aren't writing (MF03–MF07)**

- **Stage: signal two (the cause of the blind spot) and the route (where it should have been stopped).** The `words()` regex in `stylometry.py` is `[a-z0-9']+` on lowercased text, which only matches ASCII letters and digits. It ignores non-Latin Unicode like Arabic script, and emoji, so MF06 and MF07 count as zero words. MF04 (only punctuation) counts zero as well.
- Because the style signal defaults to a neutral 0.5 when it finds no words, the model score single-handedly drove the verdict. That pushed it to an extreme in both directions: near 1.0 for emoji, Arabic and the long repeated word (MF05, MF06, MF07 → AI), and near 0.0 for control characters and punctuation (MF03, MF04 → human). This input should have been refused at the route, before it reached the signals, with a guardrail that requires enough real words to score.

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
