# Changelog

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
