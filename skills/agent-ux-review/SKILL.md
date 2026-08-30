---
name: agent-ux-review
description: Use when reviewing or improving an AGENT-FACING surface — CLI help text, error messages, skill/tool/MCP descriptions, hook output, protocol frames or labels, onboarding docs, work-order briefs — by casting a cold agent as its real consumer. Triggers on "agent UX", "cold-reader review", "will an agent understand this", "review this CLI/error/skill description", "audit agent-facing surfaces". Not for human-facing UI (use IBR / persona-review) and not for code correctness review (use code review).
user-invocable: false
---

# Agent UX Review — cold-agent consumer testing for agent-facing surfaces

Agent-facing surfaces have UX. Their users are LLM agents, so the test instrument
is a cold agent cast as the surface's real consumer. Its confusion is the defect
list. Pattern proven live 2026-08-29 in the agent-rally-point typed-frame work:
a builder/reviewer loop between hosts converged each artifact in 2-3 cycles and
surfaced defects no synthetic test had found (always-on warning labels, jargon
field names, truncating channels, length-scored quality heuristics).

## The governing test

> An agent with ZERO project history must correctly interpret the surface from
> the artifact alone plus at most one discoverable command.

If interpretation requires tribal knowledge, session history, or reading source,
the surface fails — regardless of how accurate it is.

## The loop

1. **Pick the surface + consumer role.** Surface = one artifact an agent consumes
   (an error message, a `--help` screen, a skill description, a frame/label, a
   brief). Role = the agent class that consumes it ("a Codex session receiving
   this frame", "a fresh Claude session deciding whether to trigger this skill").
2. **Cast a COLD reviewer.** Dispatch a subagent (or a peer-host session for
   cross-vendor independence) with NO project context beyond the artifact itself.
   Cold context is the feature: warm reviewers can't see what's missing.
3. **Bounded verdict contract** — put ALL of this in the dispatch:
   - Role assignment ("act as the receiver-side consumer of X").
   - Step 1: RESTATE what the artifact tells you (identity, intent, what you may
     and may not do, what happens next). Misreadings here are the highest-value
     defects.
   - Step 2: attempt the task the surface exists for (interpret, choose, invoke).
   - Read-only. Do not edit files.
   - Reply **PASS or REVISE** with path:line (or field-name) evidence per finding.
     Verdict-shaped output makes the loop convergent; free prose does not.
4. **Builder fixes, reviewer re-audits.** Fresh cold reviewer per cycle (a warm
   re-reviewer has learned the jargon and will false-PASS). Converge to PASS;
   3+ cycles without convergence means the surface needs redesign, not wording.
5. **Record.** Findings that name a defect CLASS (not one string) route to the
   owning repo's backlog; the PASS artifact + final surface text are the receipt.

## Defect taxonomy (what cold reviewers reliably find)

- **Always-on warnings**: a label that fires on 100% of messages carries zero
  signal (e.g. UNVERIFIED SENDER when nothing is ever verified). Flag states
  should be quiet on the happy path, loud only on anomaly.
- **Tribal vocabulary**: field names meaningful only with repo history ("seat",
  "authority basis"). Fix: plain words, or a decoder pointer shipped in-band
  (`guide: <tool> help <topic>`) that works in any fresh checkout.
- **Imperatives without authority framing**: advisory messages written as
  commands get obeyed; if a message is non-controlling, the surface (or the
  receiving harness) must say so in words, not only in a metadata flag.
- **Channel-blind sizing**: content that truncates silently in its real delivery
  channel (pane lines, prompt limits). Fix: envelope + pointer to full text,
  spilled at SEND time, never truncated at delivery.
- **Ambiguous notation**: `participant@14392` reads as a port. Every value
  carries its unit/meaning inline.
- **Missing outcome fields**: requests without intent / goal / done-looks-like /
  follow-up protocol produce guessing receivers. Work orders declare all four.

## Iterative self-improvement wiring (other apps and plugins)

- **Per-change**: when a diff touches an agent-facing surface (help text, tool or
  skill descriptions, error strings, hook stdout, protocol labels), run one loop
  cycle on the changed surface before merge — the agent-UX analog of a UI
  screenshot check.
- **Periodic sweep**: enumerate a repo's agent-facing surfaces (bin --help,
  error catalog, skill/agent frontmatter descriptions, MCP tool descriptions,
  hook outputs) and run the loop across them; file REVISE findings as backlog
  cards. Skill and tool DESCRIPTIONS deserve priority — they drive triggering,
  so their UX failures are silent routing failures.
- **Cross-vendor pairing** when independence matters: builder on one host,
  reviewer on another (e.g. Codex builds, Claude reviews). Same-model review
  shares blind spots.

## Boundaries

- Reviewer is read-only; the builder owns edits. One builder-writer at a time.
- Cold means cold: no CLAUDE.md project lore, no session history in the dispatch.
- This skill judges comprehension and actionability, not correctness — pair with
  code review for logic and tests.
