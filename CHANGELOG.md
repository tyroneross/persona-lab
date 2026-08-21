# Changelog

## 0.5.0

A persona run becomes a durable object. `personas.json` held who a persona is
and `encounters/` held what one persona saw in one sitting, but the panel itself
— the roster, the frozen artifact, the lanes in order, what nobody could settle
— was never a thing you could open afterwards.

```
~/.persona-lab/runs/<run_id>/run.json    the machine record
~/.persona-lab/runs/<run_id>/report.md   the readable one, generated
~/.persona-lab/runs/<run_id>/notes/      anything a human or agent adds
```

- `persona run new|list|show|report|close`, backed by `lib/runs.mjs` and
  `schemas/run.schema.json`.
- History reads both directions. Encounters stay indexed by persona, because a
  persona's history ACROSS panels is what makes it worth keeping; the run
  references them by id and each encounter carries `run_id` back. So "everyone
  on this panel" and "every panel this persona sat on" are both one command.
- The freeze rule is now enforced where the run is recorded, not only in prose:
  `run new` refuses to open without `--version`, and the schema pins
  `artifact.frozen` to true.
- Lane order is validated. A debate lane cannot precede a blind lane — running
  debate first destroys the only unanchored reaction the panel will ever get,
  and it cannot be recovered.
- `run close` pools every encounter's `unanswered` into the run. That list is
  the next dispatch's agenda.
- `report.md` separates verified findings from positions. A preference is not a
  defect awaiting verification; it is a position that needs a decision. Filing
  the two together is the conflation the method exists to prevent.
- A closed run refuses new encounters, and the refusal holds: the encounter is
  still saved (a persona's verbatim is not discardable) but its pointer is
  demoted to `unlinked_run_id`, so the backlink cannot pull it into a report for
  a panel that had already closed.

## 0.4.1

Close the activation gap. `scripts/persona_usage_audit.py` over 1821 transcripts
found the skill had never been invoked and the agents never dispatched — the
plugin ships in the RossLabs-AI-Toolkit marketplace but was never enabled. The
26 sessions that used personas anyway did it by hand, so the demand was never in
question; the reachability was.

- Skill `description` rewritten against the 11 verbatim requests that should
  have fired it. Leads with "launch" (the dominant verb, 4 of 11), adds the
  observed vocabulary — dispatch, debate, interview, stress-test, in parallel,
  raw reactions separate from synthesis — and carries an explicit anti-trigger
  so it does not fire on personalization features or a solo UI review.
- Added skill §5b Debate Rounds. Users ask for personas that argue; the skill
  forbade cross-visibility. Both hold if they stay ordered: blind independent
  passes always run first and are saved, then an optional debate pass runs with
  `blind: false` and `prior_encounters_shown` naming the other personas'
  positions — never the persona's own history, which produces rationalisation
  rather than argument.
- `persona validate` now validates a persona as it will exist after save, so a
  fresh `persona new` scaffold reports only the 7 fields a human must fill
  instead of 12 errors including `id`/`created_at`/`updated_at` that saving
  mints anyway. `--strict` keeps the raw pre-save view.
- Scenarios must now carry a non-blank title and description. The scaffold
  shipped `[{title:"",description:""}]` and the validator only counted array
  length, so every persona created on the happy path saved with a required
  field that said nothing. All 6 personas in the existing library still
  validate unchanged.

## 0.4.0

Persona memory becomes executable. The encounter schema and `docs/persona-memory.md`
landed in 0.3.x as documents; nothing an agent runs actually read them. This wires
them into the CLI, the agents, the skill, and the commands.

- Added `persona encounter new|save|validate|list|show`, backed by
  `lib/encounters.mjs`. Encounters live in the global library at
  `~/.persona-lab/encounters/<persona_id>/`, beside `personas.json`, so a persona
  recalled from any repo carries its history. Append-only: a recorded
  `encounter_id` is never overwritten.
- The validator enforces the five fields the method depends on: `verbatim` is
  required (and never summarised), `conditions.viewports` must be non-empty,
  `blind` must be declared, an informed read must name its
  `prior_encounters_shown` (and a blind read must not), and a `reclassified`
  finding must carry a `verification_note`.
- Added `agents/persona-research-adjudicator.md`. The UX-researcher layer earned
  its place in the source study as an *adjudicator*, not a summariser: it verifies
  every reported defect against the artifact, marks findings confirmed / refuted /
  reclassified / unverified, and says plainly where a participant was mistaken. It
  refuses to reconstruct a missing participant from that participant's own prior
  reports.
- `persona-perspective-reviewer` now writes its encounter *before returning* and
  gets one turn: it becomes unreachable about thirty seconds after it finishes, so
  anything it cannot settle goes into `unanswered` rather than a follow-up.
- `persona-panel-orchestrator`, the skill, `/persona-lab:persona-review`, and
  `/persona-lab:run` now freeze and version the artifact before any persona sees
  it, ask everything in the first dispatch, run blind by default, and adjudicate
  before synthesis.
- The skill states the method's bound explicitly: simulated participants giving
  reactions, with no task-success or timing data.

## 0.3.0

- Added `/persona-lab:run`: autonomously drive an AI User Personas council run to
  completion — one independent subagent per persona pass, record findings,
  synthesize preserving conflicts. Hard budget gate at 20 total passes.
- Skill documents the headless council API (rosters/runs/findings/synthesis/status)
  and the autonomous-run protocol.

## 0.2.0

- Added the `persona` CLI (`bin/persona.mjs`): new/save/validate/list/show/
  search/rm/archive, roster save/list/show/rm/lenses, and panel planning.
- Added a global, recallable persona library at `~/.persona-lab/` (override
  with `PERSONA_LAB_HOME`), shared by the CLI, coding agents, and the app.
- Added `lib/library.mjs` (library + validation) and `lib/roles.mjs` (lens
  catalog with a guaranteed adversarial/red-team lens per panel).
- Schema v1.1.0: added `job_to_be_done`, `anti_goals`, and `provenance`.
- Folded research-backed guardrails into the skill and agents: hypothesis-not-
  validation stamp, mandatory red-team lens, engineered independence,
  abstain-over-fabricate, conflict-preserving synthesis, per-finding provenance.
- Wired the Next.js app repository to the shared library; `persona-plan.mjs`
  retained as the legacy planner.

## 0.1.0

- Initial dual-host Claude Code and Codex plugin.
- Added shared persona panel skill, slash command, orchestrator agent,
  perspective reviewer agent, role-selection reference, and deterministic
  roster planning script.
