# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 15:24
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `e70480df-c535-4d15-be72-b29009aa2b6f` | human | 0.298 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d4026759-eec9-4ba0-b8a2-f1cd6d0c3339` | unsure | 0.435 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `a5dee1db-aa3e-4a3f-b43b-f6554dd86ea5` | unsure | 0.521 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `8beac9c4-9650-4b54-b9cb-01576f1071c6` | unsure | 0.558 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `bd27d71d-e786-460c-a650-a6983980fea6` | human | 0.256 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `05cf12c0-901d-4f31-a6f5-64ce17be6031` | unsure | 0.428 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `9b556927-ad7f-443a-8a18-c750bbdcae4b` | unsure | 0.434 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `25c57287-87e9-4f52-9188-3f2e668dea1f` | human | 0.343 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `214e9b4a-a616-4713-bb6d-9aea6c3b2756` | unsure | 0.549 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `b2ac117f-bfd0-4c9b-bac9-b6854a9fb9c5` | ai | 0.897 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f98d1b3c-a9c6-47e2-8ca5-fe05a8d24268` | unsure | 0.541 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `4ab28e6c-5fb9-4f70-9e8d-e8eab8191f3b` | unsure | 0.687 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `7374ee42-dc1f-4f7b-aa29-85e9a52531eb` | unsure | 0.685 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `bf6a07ea-990f-4fd2-a2b3-f145d9ffccab` | unsure | 0.685 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `6d12e6d6-dfe6-459b-98f2-c5163e2df4e2` | ai | 0.788 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `fddb77f6-601f-4cfc-bb99-e76be6a27653` | ai | 0.715 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `92c154ee-2019-41a6-ad78-8e05c6771c01` | ai | 0.752 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `7eaa6a61-3e63-4db0-8253-0b8d3b3c57d4` | unsure | 0.354 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `6413b321-e090-4b2e-9ab7-8431f08d4a06` | unsure | 0.386 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `63a0e886-643f-4d09-be09-876176ace9ac` | human | 0.211 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `052720bf-5a4d-4917-bf8d-ef70442377ce` | unsure | 0.511 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `787a433f-7ec2-4265-9dac-9bcb6ea2473e` | unsure | 0.430 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `b0e06189-fd9b-48ac-a882-e7aefe3fb5b4` | unsure | 0.436 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `74c598e6-63f8-4836-a57b-f5e1c80b98a4` | unsure | 0.505 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ccc65e4a-e7d8-4de2-a735-ac7dc58888da` | human | 0.197 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `67fb7149-0016-4bf9-91d9-8671964620cf` | human | 0.197 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e0bcdb90-7fb7-4b62-8e71-d98b325054cd` | human | 0.197 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c6d65e76-f762-41a0-b0da-5fd6c847ac72` | human | 0.197 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `724ee189-7f34-4351-9512-da494bd5ba29` | human | 0.197 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "e70480df-c535-4d15-be72-b29009aa2b6f",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.2978,
  "model_score": 0.1635,
  "style_score": 0.4993,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "d4026759-eec9-4ba0-b8a2-f1cd6d0c3339",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4346,
  "model_score": 0.5943,
  "style_score": 0.195,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "a5dee1db-aa3e-4a3f-b43b-f6554dd86ea5",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5206,
  "model_score": 0.6662,
  "style_score": 0.3023,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "8beac9c4-9650-4b54-b9cb-01576f1071c6",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.558,
  "model_score": 0.6114,
  "style_score": 0.4779,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "bd27d71d-e786-460c-a650-a6983980fea6",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2557,
  "model_score": 0.3212,
  "style_score": 0.1574,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "05cf12c0-901d-4f31-a6f5-64ce17be6031",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.428,
  "model_score": 0.5727,
  "style_score": 0.2109,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "9b556927-ad7f-443a-8a18-c750bbdcae4b",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4343,
  "model_score": 0.5862,
  "style_score": 0.2064,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "25c57287-87e9-4f52-9188-3f2e668dea1f",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3425,
  "model_score": 0.2452,
  "style_score": 0.4884,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "214e9b4a-a616-4713-bb6d-9aea6c3b2756",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5486,
  "model_score": 0.7042,
  "style_score": 0.3152,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "b2ac117f-bfd0-4c9b-bac9-b6854a9fb9c5",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8975,
  "model_score": 0.9792,
  "style_score": 0.7749,
  "label": "We are confident this text was generated by artificial intelligence.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "f98d1b3c-a9c6-47e2-8ca5-fe05a8d24268",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5407,
  "model_score": 0.6175,
  "style_score": 0.4255,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "4ab28e6c-5fb9-4f70-9e8d-e8eab8191f3b",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6867,
  "model_score": 0.7387,
  "style_score": 0.6087,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "7374ee42-dc1f-4f7b-aa29-85e9a52531eb",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6852,
  "model_score": 0.8051,
  "style_score": 0.5053,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "bf6a07ea-990f-4fd2-a2b3-f145d9ffccab",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6847,
  "model_score": 0.8329,
  "style_score": 0.4625,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "6d12e6d6-dfe6-459b-98f2-c5163e2df4e2",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7883,
  "model_score": 0.8005,
  "style_score": 0.77,
  "label": "We are confident this text was generated by artificial intelligence.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "fddb77f6-601f-4cfc-bb99-e76be6a27653",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.715,
  "model_score": 0.8814,
  "style_score": 0.4654,
  "label": "We are confident this text was generated by artificial intelligence.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "92c154ee-2019-41a6-ad78-8e05c6771c01",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.752,
  "model_score": 0.8816,
  "style_score": 0.5576,
  "label": "We are confident this text was generated by artificial intelligence.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "7eaa6a61-3e63-4db0-8253-0b8d3b3c57d4",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3544,
  "model_score": 0.3223,
  "style_score": 0.4026,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "6413b321-e090-4b2e-9ab7-8431f08d4a06",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.386,
  "model_score": 0.4625,
  "style_score": 0.2713,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "63a0e886-643f-4d09-be09-876176ace9ac",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2114,
  "model_score": 0.2044,
  "style_score": 0.222,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "052720bf-5a4d-4917-bf8d-ef70442377ce",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5109,
  "model_score": 0.5943,
  "style_score": 0.3858,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "787a433f-7ec2-4265-9dac-9bcb6ea2473e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.43,
  "model_score": 0.4998,
  "style_score": 0.3253,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "b0e06189-fd9b-48ac-a882-e7aefe3fb5b4",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4363,
  "model_score": 0.6401,
  "style_score": 0.1306,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "74c598e6-63f8-4836-a57b-f5e1c80b98a4",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5053,
  "model_score": 0.5583,
  "style_score": 0.4259,
  "label": "We are uncertain about the authorship of this text; it contains mixed signals.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "ccc65e4a-e7d8-4de2-a735-ac7dc58888da",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1972,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "67fb7149-0016-4bf9-91d9-8671964620cf",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1972,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "e0bcdb90-7fb7-4b62-8e71-d98b325054cd",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1972,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c6d65e76-f762-41a0-b0da-5fd6c847ac72",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1972,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "724ee189-7f34-4351-9512-da494bd5ba29",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1972,
  "model_score": 0.0287,
  "style_score": 0.45,
  "label": "We are confident this piece was written by a human writer.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
