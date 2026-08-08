# Proposal — comprehensive personas: merge identity with an execution contract

**Status:** proposal, not implemented
**Author:** Claude (build-loop session, 2026-08-08)
**Evidence base:** two panels run against the same project four days apart — a 6-persona persona-lab panel (2026-08-04) and a 10-persona hand-authored audit (2026-08-07). Both are recorded in `~/dev/research/topics/knowledge-graphs/`.

---

## Summary

persona-lab produces good **identity** artifacts and cannot produce **evidence**. The hand-authored panel produced evidence and left no reusable artifact. Each run used the wrong half of the other's method.

The fix is additive and small: keep every existing field, add a `probe` block that says what the persona must *do*, allow authored lenses alongside library lenses, and let the roster carry the grading taxonomy it already gestures at with `measurement[]`.

---

## Evidence: what each panel produced

| | persona-lab panel (6) | Hand-authored panel (10) |
|---|---|---|
| Artifact | 22 populated fields, schema-valid, saved to `~/.persona-lab`, rostered | Prose prompt inside one report |
| Reusable | Yes — `persona show`, `--roster lenny-corpus-panel` | No |
| Provenance | Enforced (`synthetic-assumed`, `0.4`) | None |
| Adversarial lens | **Structurally guaranteed** by `selectRoles()` | Present only because the author chose it |
| Output unit | Rankings, JTBD, willingness-to-pay, abandon triggers | 92 graded verdicts with executed commands |
| Epistemic status | Preference / hypothesis | Measurement |
| Re-runnable | The persona is; the finding is not | The finding is; the panel is not |

Both were valuable. The persona-lab panel's guaranteed red-team lens produced the licensing kill-list that triggered a rights check and changed the project's commercial posture — the highest-consequence finding of the engagement. The hand-authored panel found five reproducible defects including a confident factual inversion. Neither panel could have produced the other's result.

---

## Finding 1 — the scaffold constrains output shape

The six saved personas are near-identical in shape: 4–5 goals, 4–5 frustrations, 3 motivations, 3 behaviors, 2 scenarios, 2–3 anti-goals. That uniformity is not a coincidence in the subject matter; it is the `_fill.guidance` string reproducing itself. The scaffold tells the filler exactly which lists to populate, and the filler populates exactly those lists to roughly the same depth every time.

This is fine for comparability and bad for fit. A red-team persona and a novice persona have genuinely different useful shapes — the red-team's value is concentrated in `anti_goals` and attack surface, the novice's in `frustrations` and first-run friction. The current scaffold asks both for the same six lists at the same depth.

**Recommendation:** make list fields *available* rather than *prompted-uniformly*. Keep the required set minimal (identity + primary_goal + provenance + evidence) and let the lens declare which lists it actually needs depth in.

---

## Finding 2 — the lens library is domain-narrow

All 16 lenses describe **a role inside a company evaluating a product**: novice, power user, buyer, domain specialist, PM, designer, researcher, frontend engineer, data analyst, security reviewer, CSM, sales lead, GM, content designer, accessibility, red-team.

That is a product-critique panel. It does not cover:

- consumers of a **knowledge system** (an analyst mining a corpus, a researcher testing methodology)
- **outsiders** with no product relationship (an investor reading operator testimony, a journalist verifying a quote)
- **learners** (a career switcher, a student)
- **operators** whose question is a number rather than an interface (a growth lead demanding denominators)

Concrete evidence: running `persona new` on the corpus brief auto-selected *Product manager, UX researcher, UX designer, Novice, Power user, Skeptic*. Three of six (designer, novice, power-user) were poor fits for "what platform should I build from an interview corpus," and the eventual panel discarded them and hand-authored replacements. The scaffold structure was reused; the lens selection was not.

**Recommendation:** make authored lenses first-class rather than a fallback. A lens is already just `{name, perspective, primaryQuestion, successSignal, failureSignal, adversarial?}` — permit that object inline on a persona, mark it `lens_source: "authored"`, and keep `selectRoles()` for the cases where the library fits. Optionally seed a second library group (`knowledge-system` lenses) so corpus/data/research panels have a starting set.

---

## Finding 3 — no execution contract, so panels can only opine

This is the load-bearing gap. Nothing in the schema says what a persona should **do**. So a persona-lab panel reviews an artifact by reasoning about it, and a persona-lab persona cannot be told "run this, show what you ran, and grade what came back."

The hand-authored panel's entire difference in output quality traces to six lines that were in the prompt and are absent from the schema:

1. read the quality/limits docs first
2. write N questions in-voice
3. **actually execute them; show the commands**
4. grade each ANSWERED / PARTIAL / CANNOT
5. diagnose each failure as MISSING-DATA | MISSING-CAPABILITY | PRECISION-LIMITED | WRONG-SHAPE
6. name the single highest-leverage unlock

Item 3 is what converts opinion into measurement. Item 5 is what makes findings actionable — it separates "the corpus lacks this" from "the data exists but has no query path," which imply completely different fixes.

**Recommendation:** add a `probe` block (below).

---

## Proposed schema addition

Additive only. No existing field changes meaning; no migration required for existing personas.

```jsonc
{
  // ... all 27 existing fields unchanged ...

  "lens_source": "library" | "authored",   // default "library"
  "lens": {                                 // permitted inline when authored
    "name": "Investor / market analyst",
    "perspective": "outside-analyst",
    "primary_question": "Is this testimony firsthand, dated, and did it hold up?",
    "success_signal": "Claims separate own-experience from commentary and carry dates.",
    "failure_signal": "Hearsay and firsthand accounts are indistinguishable.",
    "adversarial": false
  },

  "probe": {                                // NEW — what this persona must DO
    "must_execute": true,                   // false = opinion-only review (today's behavior)
    "surfaces": [                           // tools/data the persona is required to use
      "scripts/reasoning_query.py",
      "reasoning/ledger/*.jsonl",
      "analysis/*.csv"
    ],
    "preread": ["analysis/reasoning-layer-quality.md"],
    "questions_required": 10,
    "in_voice": true,
    "special_test": "Retrieve only own_experience claims for two companies; report manual precision.",
    "evidence_required": "show the command and its output for every verdict"
  }
}
```

And at the roster level, promote the existing `measurement[]` hint into a real grading contract:

```jsonc
{
  "name": "lenny-corpus-capability-audit",
  "measurement": {
    "verdicts": ["ANSWERED", "PARTIAL", "CANNOT"],
    "failure_causes": ["MISSING-DATA", "MISSING-CAPABILITY", "PRECISION-LIMITED", "WRONG-SHAPE"],
    "require_unlock": true,
    "require_evidence": true
  }
}
```

`measurement[]` is currently a free-text array (`["Task completion","Comprehension","Friction","Trust","Risk","Business fit"]`). Accepting either the array (legacy) or this object (graded) keeps it backward-compatible.

---

## Worked example — the merge applied

The investor persona from the hand-authored panel, expressed in the proposed shape. Identity from persona-lab's model, probe from the audit prompt:

```jsonc
{
  "schema_version": "1.2.0",
  "name": "Dana Reyes",
  "archetype": "Investor / market analyst",
  "role": "Early-stage investor using operator testimony as primary-source signal",
  "summary": "Reads practitioner interviews as dated primary evidence; separates firsthand accounts from commentary before acting on either.",
  "primary_goal": "Establish what operators actually said, when, and whether it held up.",
  "job_to_be_done": "When evaluating a sector thesis, I want dated firsthand operator claims separated from hearsay, so I can weight them honestly.",
  "goals": ["Separate own-experience from commentary", "Date every claim", "Detect emerging themes before consensus"],
  "frustrations": ["Hearsay presented as firsthand", "Undated claims read as current", "Trend charts built on partial years"],
  "anti_goals": ["Will not cite a claim whose speaker relationship is ambiguous"],
  "lens_source": "authored",
  "lens": {
    "name": "Outside analyst",
    "perspective": "outside-analyst",
    "primary_question": "Is this testimony firsthand, dated, and did it hold up?",
    "success_signal": "Firsthand and commentary are separable; dates are on the claim, not just the episode.",
    "failure_signal": "A commentator's observation is indistinguishable from an operator's own account.",
    "adversarial": false
  },
  "probe": {
    "must_execute": true,
    "surfaces": ["scripts/reasoning_query.py", "analysis/org-experience-bindings.csv", "analysis/nodes-concepts.csv"],
    "preread": ["analysis/reasoning-layer-quality.md", "analysis/org-layer-quality.md"],
    "questions_required": 10,
    "in_voice": true,
    "special_test": "Pull own_experience rows for two companies; hand-check each; report precision. Then establish one 2022-2026 trend and say whether it is trustworthy.",
    "evidence_required": "show the command and its output for every verdict"
  },
  "evidence": [{ "source_type": "synthetic", "summary": "Authored lens, not grounded in user research.", "confidence": 0.4 }],
  "provenance": "synthetic-assumed",
  "confidence": 0.4,
  "tags": ["investor", "outside-analyst", "capability-audit"]
}
```

That persona is simultaneously **recallable** (persona-lab's contribution) and **executable** (the audit's contribution). Run twice against a changed corpus, it produces comparable measurements rather than fresh opinions.

---

## Why this matters beyond one project

A capability audit is only useful if you can re-run it after fixing what it found. The 2026-08-07 audit produced 92 graded verdicts and five confirmed defects — and cannot be repeated with the same panel, because the panel existed only as prose inside a dispatch. Registering personas with probes turns a one-time audit into a regression suite for a product's *usefulness*, alongside the test suite that covers its correctness.

That is the same discipline the audited project applied to its extractors: freeze the instrument, then measure. persona-lab already stores the instrument. It just doesn't store what the instrument is supposed to do.

---

## Suggested sequence

1. `probe` block + `lens_source`/inline `lens` — additive schema bump to 1.2.0, no migration.
2. Roster `measurement` object form (accept both shapes).
3. CLI: `persona new --probe` to scaffold the probe block; `persona panel --execute` to emit dispatch-ready briefs from a roster.
4. Optional: a second lens group for knowledge-system/outsider/learner perspectives, so `selectRoles()` has something to select when the brief is not a product critique.
5. Register the ten audit personas against the new shape as the first comprehensive roster.
