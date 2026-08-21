# Changelog

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
