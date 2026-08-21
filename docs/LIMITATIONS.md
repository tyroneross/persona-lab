# What this method has not earned

Read this before treating anything in persona-lab as established practice.

The rest of this repo is written in a declarative voice — "a first impression is
a non-renewable resource", "blind passes always run first". That voice is a
design stance stated plainly so it can be followed and argued with. It is not a
report of validated findings, and almost none of it has been measured.

If you are an agent that just loaded this plugin: the schemas will be enforced
against you, the CLI will refuse things, and the prose will sound settled. Treat
the enforcement as **this project's opinion, encoded so it stays consistent** —
not as evidence that the opinion is correct.

---

## Provenance of every load-bearing claim

| Claim | What is actually behind it |
|---|---|
| Encounter memory, the blind/informed split, the adjudicator role, "ask everything in the first dispatch", "freeze the artifact" | **One study.** Six personas, one artifact (The Fact Refinery), one day, 2026-08-21. Raw material in `encounters/_source-study-2026-08-21/`, ~1,400 lines. No replication, not blind, effort and model unpinned. |
| Subagent eviction at ~30s | Observed once in that study; the `pbe = 30000` constant was read out of a Claude Code binary that has since changed versions. **Not re-verified.** If this number is wrong the encounter-before-return rule loses its main justification (though it stays defensible on durability grounds alone). |
| Persona-lab usage: 22 plugin events vs 335 ad-hoc across 4,781 transcripts | **Measured.** `scripts/persona_usage_audit.py`, both hosts. The strongest evidence in the repo — and it measures adoption, not whether the method works. |
| Recall scope defaults across the 16 lenses (novice `none`, architect `all`, …) | **Asserted.** Assigned by reasoning about which roles have cumulative versus non-renewable value. Zero evidence that an `all`-scope architect produces better review than a `none`-scope one. |
| `none` as the global default | **Asserted**, from an asymmetry argument: wrongly-fresh is recoverable, wrongly-anchored is not. The argument is sound; the premise that anchoring meaningfully degrades a persona review here has not been tested. |
| "Panels are for spread, not consensus" | Single study, plus one earlier 10-persona audit (`lenny-podcast-transcripts`, 2026-08-07) that reached the same conclusion. Two observations, same author, same year. |
| Required adversarial lens counters LLM positivity bias | Borrowed from published concern about model sycophancy. **Never tested in this system.** No run has been compared with and without it. |

## Never run in anger

As of 0.7.0 the live library holds **6 personas, 0 encounters, 0 runs**.

Everything added in 0.4.0–0.7.0 — encounter memory, run objects, recall scopes,
outcome lessons — has been exercised only by its own tests. No real panel has
been composed through it end to end. The first genuine run should be treated as
a shakedown, not a result.

## What would actually validate this, and does not exist

These are the gaps that matter most, roughly in order of how much they would
change your confidence.

**1. No calibration against real humans.** Nothing has ever compared a persona
panel's findings to what actual people did with the same artifact. Synthetic
personas could be wrong in a consistent direction — over-indexing on things
models notice, blind to things people trip on — and every control in this repo
would still pass. This is the foundational gap; everything below is secondary.

**2. No baseline.** The method has never been run against a cheaper alternative
on the same artifact: a heuristic checklist, a single strong reviewer, or one
model asked for six perspectives in one pass. "Findings no checklist would have"
is asserted in the method assessment and was never tested against a checklist.

**3. Nothing measures whether personas actually diverge.** Independence is
engineered (separate contexts, no shared transcript) but never verified. Two
personas could return near-identical findings and nothing would flag it. A
simple distinctness metric over encounter findings would catch it.

**4. The adjudicator is un-adjudicated.** `persona-research-adjudicator` sets
`verified: confirmed | refuted | reclassified` and no independent check grades
it. It is an LLM marking an LLM's homework, and it is the exact place a
confident wrong call gets laundered into a "verified finding".

**5. Model tier effects unmeasured.** The 10-persona run was Haiku, the source
study was mixed. Nobody knows whether tier changes what a persona notices. Since
per-persona model assignment is the top unmet feature request, this gap will get
worse before it gets better.

**6. Panel size has no basis.** 3–6 lenses recommended, 10 used once. The numbers
came from judgment, not from a curve of findings versus panel size.

**7. No cost accounting.** Every pass is a real LLM call. Nothing tracks tokens
per run or findings per token, so "was this panel worth it" can only be answered
by feel. `persona run lesson` records a verdict but not a cost.

**8. Encounters have no retention policy.** They accumulate forever. A persona
with `recall: all` and 200 encounters will overflow any dispatch context, and
`buildRecallBriefing`'s `limit` (default 6) silently truncates by recency with no
notion of which memories matter. Recency is a weak proxy for relevance.

**9. The usage-audit classifier is unvalidated.** `persona_usage_audit.py` uses
regex heuristics to split plugin from ad-hoc use. It was hand-corrected once when
it over-counted, but has never been scored against a hand-labeled sample, so its
precision and recall are unknown. Treat its counts as indicative, not exact.

**10. Reconstruction is undetectable.** `permittedEncounters` filters on persona,
artifact, and project with no provenance or age check. A fabricated encounter is
indistinguishable from a real one at recall time. The project's answer is a rule
("never back-fill") rather than a mechanism, and a rule is only as good as the
agent following it. A `provenance` field on encounters would make it structural.

## What is genuinely solid

Not everything is soft, and over-correcting is its own failure:

- **The adoption measurement** (#3 in the provenance table) is real data over a
  real corpus and reproducible in about 100 seconds.
- **The durability argument** for writing encounters before returning holds
  regardless of the exact eviction timing: a return value that is the only copy
  of the work is fragile for reasons that have nothing to do with 30 seconds.
- **The disagreements the source study surfaced** (experts calling tooltips dead
  weight while novices depended on them) are real observations from that study,
  whatever their generality.
- **The enforcement is consistent.** Whether or not the opinions are right, they
  are applied uniformly rather than remembered unevenly, which is what makes them
  falsifiable at all.

## If you are extending this

Prefer work that closes a gap above over work that adds a feature. The method's
bottleneck is not capability — it is that almost nothing here has been checked.

When you add a claim to the docs, add its provenance to the table above in the
same commit. A claim that enters this repo without one becomes indistinguishable
from a validated finding within about two commits, which is how the current
declarative voice happened in the first place.
