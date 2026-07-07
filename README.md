# Persona Lab

Persona Lab turns a request into a focused AI persona panel, and keeps the
personas it generates in a recallable, global library. It ships three entry
points over one engine:

- **CLI** (`persona`) — generate, save, recall, and plan panels from any repo.
- **Plugin** (Claude Code + Codex) — a skill, command, and agents so coding
  agents can run persona reviews.
- **App** — the `AI User Personas` Next.js UI reads and writes the same library.

It codifies this workflow:

1. Capture the request.
2. Recall an existing roster/personas, or select fresh perspectives.
3. Generate personas (one distinct lens each), grounded in real evidence where
   available and labelled as hypothesis where not.
4. Run independent persona reviews, then synthesize while preserving conflicts.
5. Save reusable personas and rosters for next time.

Output is a **hypothesis for review, not validated user research**. Every panel
requires at least one adversarial (red-team) lens, runs each persona
independently to avoid groupthink, and lets personas abstain rather than
fabricate.

## Install the CLI

From this plugin directory:

```bash
npm link          # exposes `persona` on your PATH
# or: npm install -g .
```

The library lives at `~/.persona-lab/` by default (override with
`PERSONA_LAB_HOME`). It is global: save a persona once, recall it from any repo.

```text
~/.persona-lab/
  personas.json          { schema_version, personas[] }
  rosters/<slug>.json     named lens/persona presets for a use-case
```

## CLI

```bash
persona new "review the onboarding flow for enterprise admins" --count 4
#   selects distinct lenses (>=1 adversarial), emits fill-in scaffolds + a
#   generation prompt + a measurement plan. Add --json for the scaffolds.

persona save persona.json          # validate + persist to the library
persona validate persona.json      # schema check only (exit 1 on failure)

persona list [--tag t] [--role r] [--status s]
persona show <id>
persona search "audit"
persona archive <id>   |   persona rm <id>

persona roster save "Enterprise rollout review" \
  --lenses red-team,buyer,accessibility,novice \
  --personas persona_dana-okoro_57144a1d \
  --use-case "Reviewing a B2B feature before enterprise rollout"
persona roster list | show <name> | rm <name> | lenses

persona panel "review the settings redesign" --level medium
persona panel --roster "Enterprise rollout review" --level high

persona home        # print the library path
```

The CLI is the deterministic substrate: it owns the library, schema validation,
lens selection, and review planning. Generating persona *content* and running
the review are done by the LLM host (a coding agent, the skill, or Codex), which
calls the CLI to persist and recall. No API key is needed by the CLI.

### Review levels

- `low` — 3-4 lenses, single independent pass. Cheap first look.
- `medium` — 4-6 lenses incl. required red-team, independent passes + synthesis.
- `high` — 6+ lenses, independent passes + adversarial verification of critical
  findings + measurement rigor.

## Plugin (Claude Code and Codex)

The plugin content is host-neutral; both hosts load the same command, agents,
skill, references, and CLI.

```bash
claude --plugin-dir ./plugins/persona-lab
codex  --plugin-dir ./plugins/persona-lab
```

Slash command:

```text
/persona-lab:persona-review Review the onboarding flow for a founder persona.
```

## Structure

```text
persona-lab/
  package.json                     bin: persona -> bin/persona.mjs
  bin/persona.mjs                  CLI
  lib/library.mjs                  global library (personas + rosters) + validation
  lib/roles.mjs                    lens catalog + selection (>=1 adversarial)
  commands/persona-review.md
  agents/persona-panel-orchestrator.md
  agents/persona-perspective-reviewer.md
  skills/persona-lab/SKILL.md
  skills/persona-lab/references/persona-selection.md
  scripts/persona-plan.mjs         legacy first-pass planner (superseded by `persona new`)
```

## Persona schema

Canonical contract: `schemas/persona.schema.json` (v1.1.0). Load-bearing
fields are goals, behaviors, frustrations, motivations, needs, and
`job_to_be_done`; demographics are optional decoration. `provenance`
(`proto | qualitative | synthetic-grounded | synthetic-assumed`) and `anti_goals`
make the persona's basis and abandonment triggers explicit.
