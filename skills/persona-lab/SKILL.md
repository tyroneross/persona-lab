---
name: persona-lab
description: Use when the user asks to spin up personas, test UI through AI user personas, review a product from multiple perspectives, or turn a request into a task-specific persona panel with plan, measurement, launch, and report-back.
---

# Persona Lab

## Objective

Turn a user query or request into a focused persona panel that can review a UI,
product, workflow, feature plan, API surface, or research artifact.

This skill is not a replacement for real user research. It is a structured
synthetic review method for finding likely product, usability, business,
technical, and risk issues before or between real research cycles.

Synthetic personas are legitimate for hypothesis generation and critique, never
for validation. Every panel output is a hypothesis, not real-user evidence.
Stamp the report as "hypothesis, not validation" and never present a persona
finding as proof of real user behavior.

## Workflow

### 1. Capture the Request

Restate the request in one sentence.

Identify:

- Target artifact: app, screen, workflow, PRD, repo files, screenshot, data,
  logs, design, or prompt.
- Decision being supported: ship, revise, prioritize, scope, test, debug,
  compare, or explain.
- Primary user outcome.
- Constraints: timeline, platform, audience, business model, compliance,
  existing plan, or implementation limits.

### 2. Select Persona Perspectives

Prefer 4 to 6 sharply distinct lenses unless the user specifies a different
count. Fewer, well-separated lenses beat many overlapping ones.

Recommended default critique lenses:

1. Novice / first-run user.
2. Power user / expert.
3. Skeptic / adversary / red-team. REQUIRED in every panel.
4. Accessibility / constraint-bound user.
5. Decision-maker / buyer.
6. Domain specialist.

Selection rules:

- Pick perspectives by MECE coverage of goals, jobs-to-be-done, and risk, not by
  demographics.
- Goals, behaviors, and job-to-be-done are the load-bearing persona elements.
  Demographics are decoration and invite stereotyping. Keep them optional and
  omit unless the topic requires them.
- Each persona must represent a distinct lens, not a superficial variation of
  another.
- Prefer roles with decision power over generic labels. For example:
  `Enterprise security admin` is better than `IT person`.
- Always include at least one adversarial / red-team lens. This is not optional.
  It is the structural counter to LLM positivity bias.
- Include accessibility or inclusive-design review when the artifact is a UI,
  workflow, form, onboarding path, dashboard, or content-heavy surface.
- Use internet research when role choice or context depends on current market,
  company, competitor, regulation, pricing, trend, or domain facts.

Use `references/persona-selection.md` for the critique lenses, the fuller role
catalog, and the independence and anti-sycophancy rules.

### 3. Check Task, Intent, And Execution Access

Before launching the review, verify what is available.

Check for:

- Files or repo paths to inspect.
- Running app URL or local dev server.
- Screenshots, recordings, analytics, logs, support tickets, survey data, or
  research notes.
- Browser, shell, web, or data access.
- User-provided success criteria.

If access is missing but the review can proceed, label the review as synthetic
and list access gaps. If access is required to avoid a misleading answer, ask
one concise blocking question.

Do not claim that you tested a UI, searched the web, inspected analytics, or
verified behavior unless the relevant tool was used or the evidence was
provided.

### 4. Plan Steps And Measurement

Define measurement before the persona passes.

Use this minimum measurement set:

- Task completion: can the persona complete the intended action?
- Comprehension: does the persona understand what to do and why?
- Friction: what slows, blocks, or confuses the persona?
- Trust: what makes the persona doubt the product, data, or next step?
- Risk: what could create privacy, security, legal, operational, or brand harm?
- Business fit: does the experience support the desired product outcome?

For each persona, define:

- Primary question.
- Success signal.
- Failure signal.
- Anti-goals: what would make this user abandon, distrust, or reject the
  product.
- Evidence to inspect.

### 5. Launch The Persona Panel

Engineer independence. Distinct personas collapse into one homogeneous voice
when they share a transcript or a status hierarchy. Run each persona's critique
in a separate context with no shared transcript and no visibility into other
personas' findings. Synthesize only after all independent passes complete.

Each persona must be allowed and instructed to abstain. LLMs fabricate roughly
half the time instead of admitting uncertainty. A persona that cannot judge a
point from the available evidence must answer "cannot judge from available
evidence" or "no concern" honestly, rather than invent a finding.

Preferred launch path when subagents are available:

1. Use `persona-panel-orchestrator` to select personas and measurement.
2. Launch `persona-perspective-reviewer` once per persona, each with the
   assigned persona, artifact, and measurement criteria, and no knowledge of the
   other personas or their findings.
3. Keep each review independent until synthesis.

Fallback launch path:

1. Run sequential persona passes in the main conversation.
2. Reset assumptions between passes and do not carry one persona's findings into
   the next.
3. Keep notes separated by persona before synthesis.

For UI work, inspect actual files and use browser/screenshot verification when
the app is available. For strategy, market, regulated, or competitor-sensitive
work, research current sources before making current-state claims.

### 6. Report Back

Use bottom-line-first structure.

Required report:

```text
Bottom line:
What was inspected:
Persona roster:
Measurement:
Priority findings:
Persona-specific findings:
Access gaps and assumptions:
Recommended next actions:
```

Findings should include:

- Severity: critical, high, medium, or low.
- Evidence: file, screen, quote, source, screenshot, command, or observed
  behavior.
- Provenance: evidence-grounded or model assumption. Label every ungrounded
  finding as an assumption.
- Impact: why the persona cares.
- Fix: concrete recommendation.
- Confidence: high, medium, or low.

Keep the synthesis decisive, but preserve conflicts as explicit tradeoffs rather
than averaging them away. For example: power user wants density versus novice
wants simplicity. Preserve dissenting critical findings when one persona flags an
issue that others do not.

Stamp the report as "hypothesis, not validation". These are synthetic
perspectives, not real-user evidence.

## Review Levels

- low: 3 to 4 lenses, single independent pass, cheap. Fast first-look critique.
- medium: 4 to 6 lenses including the required red-team lens, independent passes
  plus synthesis. The default.
- high: 6 or more lenses, independent passes plus adversarial verification of
  critical findings plus measurement rigor.

## Persona CLI

The `persona` CLI is the deterministic substrate: it selects distinct lenses,
persists and recalls personas and rosters, and scaffolds the review plan. The
generative and review steps are yours as the LLM host; call the CLI to plan,
persist, and recall.

Recall before generating. Reuse saved personas and rosters instead of
regenerating from scratch:

```bash
persona list [--tag <tag>] [--role <role>] [--status <status>]
persona show <id>
persona search "<query>"
persona roster list
persona roster show <name>
```

Generate and save. `persona new` emits distinct lens skeletons plus a generation
prompt and a measurement plan; you fill the persona content, then save so it is
reusable across repos:

```bash
persona new "<brief>" [--count N] [--roster <name>]
persona save <file.json|->
persona validate <file.json|->
```

Scaffold the review. `persona panel` emits the review plan (lenses,
measurement, independence rules, and guardrails) for you to execute:

```bash
persona panel "<topic>" [--roster <name> | --auto] [--level low|medium|high]
```

Other commands:

```bash
persona rm <id>
persona archive <id>
persona roster save <name> --lenses a,b,c [--personas id1,id2] [--use-case "..."]
persona home
```

Saved personas and rosters live in the global library at `~/.persona-lab/`, so a
roster saved in one repo is recallable by name from any other. Treat CLI output
as a starting point, not the final review.

The legacy planner `node plugins/persona-lab/scripts/persona-plan.mjs
"<request>"` still exists but is superseded by the `persona` CLI.

## Autonomous council runs (AI User Personas app)

When the AI User Personas app is running, you can drive a full council review to
completion over its HTTP API instead of reporting inline. Use the
`/persona-lab:run` command, or drive the API directly against
`${APP_URL:-http://localhost:3000}`:

```text
POST /api/councils/rosters            build a roster from saved library personas
POST /api/councils/runs               create a run {roster_id, request, level, runs_per_persona}
GET  /api/councils/{run_id}           read the bundle + command packet
PATCH /api/councils/{run_id}/status   ready -> running
POST /api/councils/{run_id}/findings  record findings (validated, batch-capable)
PUT  /api/councils/{run_id}/synthesis record synthesis; advances the run to complete
```

Drive it exactly as a manual panel: one INDEPENDENT subagent per persona pass
(no shared transcript), abstain over fabricate, at least one adversarial pass,
and preserve conflicts as `dissent_map` in the synthesis.

Hard budget gate: `total_passes = personas x runs_per_persona`. If it exceeds 20,
stop and get explicit confirmation before spawning subagents — each pass is a
real LLM call. Output is hypothesis, not validation.
