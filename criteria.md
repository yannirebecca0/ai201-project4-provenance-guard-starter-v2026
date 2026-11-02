# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

Of 10 completely human-written personal essays or poems submitted across three test trials, at most 1 is incorrectly labeled as high-confidence AI.

**Why this target:** 
Accusing an authentic human writer of cheating is the most damaging failure mode for a publishing platform. A false positive breaks trust permanently, whereas a missed AI detection simply lets a piece slip through.

---

## 2.

Clearly AI-generated text and clearly human-written text must produce average combined confidence scores separated by at least a 0.40 margin across standard test runs.

**Why this target:** 
If the signals don't cleanly discriminate between the two extremes, the system will hover in a muddy middle ground where confidence scores are uninterpretable and actionable labels become arbitrary.

---

## 3.

All three labels (`high-confidence AI`, `high-confidence human`, and `unsure`) must be reachable given a diverse set of test inputs spanning the 0.0 to 1.0 confidence spectrum.

**Why this target:** 
Ensures that no threshold range is completely blocked off by dead code, and that the "unsure" band actually functions as a buffer zone for borderline writing instead of instantly defaulting to a binary verdict.

---

## 4.

100% of appeals submitted with a valid `content_id` and reasoning string successfully update the item's status to `under_review` and append the record to the audit trail without throwing an error.

**Why this target:** 
Writers who are flagged incorrectly must have a reliable, frictionless fallback mechanism. A broken or silent appeal path destroys accountability when the automated detection gets it wrong.

---

## 5.

If an incoming submission contains empty text, missing keys, or text exceeding 10,000 words, the endpoint gracefully returns a `400` status code rather than crashing the server or hanging.

**Why this target:** 
Production backends must be resilient against malformed client payloads or abuse. Crashing on bad inputs would allow simple client errors or denial-of-service attempts to take down the verification service.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
