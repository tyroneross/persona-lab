# P2 — Strategy Hiring Manager Review: Atomize AI "Fact Refinery" snapshot

Reviewed at `[local snapshot: eval-snapshot.html]`, desktop (1920px) and mobile (390px), FLOOR and BLUEPRINTS tabs. Verified with IBR `screenshot`, `scan`, `observe`, `interact`, and `interact_and_verify` (persistent `session_start` refused to connect on this instance — noted below as a tooling limitation, not held against the page).

---

## 1. Ten seconds in — worth my time?

Yes, provisionally. The subhead earns it: **"Atomize reads the day's AI news and research, then keeps only the facts it can prove with a verbatim quote."** That's a real claim about a real mechanism, not marketing fog. The frame — "a working scale model" of a "PIPELINE UNIT" — tells me the builder is choosing to show me a toy with real wiring underneath rather than a static feature list. That's the right instinct for someone who's supposed to sit between business and engineering.

What almost lost me: the H1 itself — **"THE ATOMIZE AI PLANT REFINES RAW TEXT INTO INTELLIGENT NEWS"** — is empty calorie copy. "Refines," "intelligent news" — that's the marketing register the subhead then contradicts in a good way. First impression is mixed: strong instinct, weak headline.

## 2. What decision could I actually make after this?

None that I'd bet money on, and the page itself all but says so. Section 02 is titled **"THIS IS THE BEST EVIDENCE ON THE PAGE, AND IT STILL IS NOT SHIPPING."** — a builder handing me their own decision-quality caveat. That's the most honest sentence on the page, and it tells me the one decision on offer (should the intent-cascade router ship?) is explicitly *not* mine to make from this page — the team already declined to ship it after measuring it.

The closest thing to a decision I could form an opinion on: whether the $8/month cost-per-quality-floor tradeoff (visible on the FLOOR tab) is defensible at whatever scale this is meant to hit. But the page never tells me the scale, the query volume behind the $8, or what breaks that number. So even that's a "would need one more number" decision, not a "make it now" decision.

## 3. Where does it explain a tradeoff honestly, vs. sell a result?

**Honest tradeoff**, section 02, in full: *"A three-tier classifier can route a search query more accurately than the code running today. The team measured it carefully on real production traffic, then decided not to turn it on."* Paired with a real number — **"45 of 64 queries retrieve differently. 70.3%."** — and a toggle stuck at **OFF**. This is the single best paragraph on the page. It shows a team that built something better and chose not to ship it, and says why in the surrounding copy (cost/complexity implied, not fudged). That's the honesty I hire for.

**Selling a result**, FLOOR panel, "Gate Power": *"Switching this off lifts the gate arm clear of the flow. Everything passes, including text that should have been rejected."* — fine, that's honest about failure mode. But the **H1 and section 01 header** ("SELECT INPUTS AND SEE HOW DATA IS PROCESSED BY THE ATOMIZE FACTORY") oversell the interactivity: the controls it's describing don't actually respond to input (see #6). Describing a slider as something I can "select" and "see" processed when clicking it does nothing is the page selling an experience it doesn't deliver.

## 4. Invented vs. measured labels — rigour or excuse?

Rigour, and it's the best design decision on the page. The BLUEPRINTS tab states the taxonomy up front: **"Every component carries a badge for how its parameters are known: `MEASURED` a number was actually recorded, `REASONED` a written rationale exists in the repository, `INFERRED` we read the reason from the code, nobody stated it, `DEFAULT` a library or bare constant nobody tuned, `BUILT NOT WIRED` built and never switched on, `NO RECORD` no rationale exists in the repository."**

That's a provenance taxonomy for claims — exactly the discipline I want from someone translating engineering to business. It doesn't read as an excuse because it's specific and falsifiable per-component, not a blanket disclaimer. The footer reinforces it without hedging: *"Every parameter on this page... is real from the Atomize codebase. The particles, the throngs and the events are synthetic."* Two sentences, clean split between what's real and what's staged. I believe it more because they didn't try to blur the line.

The one place it *could* tip into excuse: the metrics row on FLOOR shows a `96%` "trust score" tile alongside `$8.00 cost/mo` and several `0` counters (articles fed, queries cached, vault rejects) with no visible badge on that specific tile distinguishing measured-from-synthetic in the screenshot at a glance — I'd want to confirm in an interview that the trust-score number itself carries the same badge discipline as the narrative text around it, since it's the single most persuasive-looking number on the page.

## 5. What this tells me about the builder, and what I'd probe

**What it tells me:** this person thinks in systems, not features. They built a real provenance taxonomy for their own claims, they show a rejected-but-superior design (the cascade router) instead of hiding it, and they map every simulated UI element to its production counterpart in section 04. That's rare — most builders show me the demo that worked, not the one that got benched. It also tells me they value legibility over polish: the mono-font "IT DRIVES:" / "IT RESETS:" annotations on every control are an unusual, deliberate choice to expose causality instead of just having a working slider.

**What it also tells me:** they either ran out of time or didn't prioritize making the demo controls actually work (see #6) — and shipped it anyway with confident, complete-sounding copy above those controls. That's a real signal about whether "done" means "true" or "looks true" under this person.

**What I'd probe:**
- "Walk me through why the demo controls don't respond to clicks — was that a scope cut, a bug, or intentional (state locked for the eval snapshot)?" Their answer tells me whether they know the gap exists and can defend the call, or whether they didn't know.
- "The cascade router tested 45/64 queries differently and you didn't ship it. What was the actual blocker — cost, latency, confidence, or something else the page doesn't say?"
- "Who is the $8/month number for — one query, one day, one org? What breaks it at 10x volume?"
- "Show me one `NO RECORD`-badged component and tell me what you'd need to move it to `REASONED`."

## 6. Visibly broken / misaligned / cut off

All observed at **desktop 1920px** unless noted, verified via IBR `scan` (structured DOM/handler audit) and `interact_and_verify` (live click attempts):

- **The demo controls do not work.** IBR's static scan flagged 84 of 90 interactive-looking elements as `handler-integrity/fake-interactive` — "looks interactive (role/tag/cursor) but has no handler." I verified this live, not just statically: attempted clicks on "Run a query," "Research paper PDFs" (source checkbox), "Inspect a node," "RUN THE DAY," "Quality Floor" (slider), and the "What-if" mode toggle all failed with `not actionable: not visible (hidden or covered)` or `not resolvable`. Only the **FLOOR / BLUEPRINTS** tab switcher actually has a working handler and was confirmed live (element diff of 700+ nodes, real screenshot change). Every "operate the gates" instruction in the copy is currently aspirational.
- **Touch targets below minimum on desktop too:** the `DEFAULT` badges (e.g. next to "Quality Floor," "Gate Power") measure 60×21px against IBR's 24×24px minimum — flagged twice independently by the scan.
- **Contrast:** 14 of 15 checks passed; one element fails (not isolated in this pass — flag for a follow-up contrast-specific scan before ship).
- **Small-print legend rows** (the `quality_below_floor` / `known_low_field` / etc. chip row under the FLOOR metrics, and the reason-code manifest) run at a very small size relative to the rest of the page's type scale — legible in my screenshot at 1920px but this is the kind of row that will be the first thing to break at 1280px or in a laptop-scale demo during an actual interview.
- **Mobile (390px):** page holds together — no obvious overlap, cut-off, or truncated text observed in the full-page capture. The header wraps cleanly, the tab switcher stays anchored top-right, and the pipeline diagram and metrics grid stack vertically without collision. Genuinely solid responsive behavior; better than the desktop interactivity story.

## 7. The single change that would most improve it for me

**Wire the FLOOR tab's controls to their own stated function, or relabel the section to say plainly that it's a static walkthrough.** Right now the page's strongest asset — its honesty about what's measured vs. invented — is undercut by a UI that claims "Operate the gates below, close a hopper, or loosen a threshold, and watch what the plant does" and then doesn't respond when I do exactly that. For a hiring manager, a demo that oversells its own interactivity is a worse signal than a demo that had no interactivity claim at all, because it's the same gap between claimed and actual state that the "MEASURED vs. INFERRED vs. NO RECORD" taxonomy exists to prevent. Fix the mismatch between what section 01 promises and what the DOM delivers, and this goes from "promising but unfinished" to "the real thing."
