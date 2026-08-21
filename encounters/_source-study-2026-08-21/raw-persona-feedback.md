# Raw persona feedback, verbatim

Study object: The Fact Refinery, frozen snapshot `eval-snapshot.html`, tested 2026-08-21.
Method: six personas, no prior context, each drove the live page with a real browser at phone
(390x844) and desktop (1440x900) widths. Each was told to be blunt, to quote the exact phrase
that lost them, and to say plainly if they only enjoyed the visuals without learning anything.

These are the unedited reports. Synthesis lives in a separate file so the source stays checkable.

---

## P1. Technical recruiter
Non-engineer. Places senior engineers and AI staff. Four minutes between calls. Phone first.

**1. First 30 seconds on the phone.** I thought it was a game or an interactive demo, not a resume
piece: "The Fact Refinery," "plant," "hoppers," "chutes." I couldn't tell what he actually built
until I scrolled several screens down and hit real words like Postgres, pgvector, and Vercel. My
honest first reaction was "cute, but where's the work?"

**2. Two sentences for a hiring manager, in my words.** He built a system that pulls in AI news from
five different sources, checks every fact against the original text before keeping it, and only pays
for AI processing on stuff that passes. Then he wrapped it in an interactive "factory" toy so you can
flip the switches yourself and watch what gets rejected and why.

**3. What made me think he's strong.** The stats that update live when you click things: "11 articles
fed, 1 dupes folded, 25 facts kept, 28 facts rejected," and then a breakdown by real reason code
("10 quote not grounded," "4 confidence < 0.5"). That's not a mockup, that's a running counter
reacting to my clicks. Also the "28 better, 4 worse, 13 neutral" stat on one of his experiments, a
real before/after test on his own change. That's the kind of number an engineer shows when they
actually measured something, not when they're guessing.

**4. Where I got lost or felt talked down to.** The "WHAT-IF LEVERS" block, hard. Terms like
"Reciprocal Rank Fusion at k=60," "HNSW to IVFFlat," commit hashes like "14ee1f714," and "RAGAS
run... needs a database, Groq and a curated gold set." I don't know what any of that means and the
page doesn't try to tell me. I don't know what "vector leg" means either, and the page's own
definition, "Vector search finds passages by meaning rather than by matching words," didn't fully
land for me. That whole middle section reads like it's written for another engineer reviewing his PR,
not for someone deciding whether to put him in front of a client.

**5. Phone-specific frustration.** I tapped "FEED ONE ARTICLE" and "RUN A QUERY" and nothing visibly
happened on my screen. The counters that changed were several scrolls away, so it felt broken until I
scrolled up. The top nav tab is cut off on phone, it reads "BLU" instead of "BLUEPRINTS." And in the
levers section, source text like "prisma/migrations/20251013000653_upgrade_to_hnsw_inde..." runs off
the right edge of the screen, clipped. Also, the same sentence, "Closing this valve seals the hopper.
No new articles fall from it until you open it again," repeats five times back to back. That's a lot
of scrolling for one idea.

**6. Would I forward it?** Yes, but with a caveat in my note. I'd say: "This candidate clearly has a
real, running system with actual measurement discipline, not just claims. The page is overbuilt as a
portfolio piece though; you'll want to skip past the middle 'levers' section, it's pure
engineer-to-engineer detail. Worth a call." I wouldn't forward it cold without that framing, because
on its own the middle third would make a non-technical hiring manager bounce.

---

## P2. Strategy hiring manager
Leads a corporate strategy function. Technically literate, does not build. Hires for judgment.

**1. Decision-making ability demonstrated.** One real instance, buried on desktop only. "Intent
Cascade routing" shows a live A/B: "28 better, 4 worse, 13 neutral" across 64 queries, then "45 of 64
queries retrieve differently, 70.3%. This size is the stated reason the flag stays off." That's a
candidate choosing not to ship a net-positive change because blast radius was too large to trust, a
real tradeoff, with the number that drove it. Everything else on the page is inventory (a labeled
list of what exists), not a decision (why one thing was chosen over another).

**2. Rigour or hedging.** Rigour. The taxonomy, MEASURED / REASONED / DEFAULT / BUILT NOT WIRED / NO
RECORD, is a provenance system, not a disclaimer. "This axis was never measured. Commit 52d7ee93f: a
live RAGAS run never happened, since it needs a database, Groq and a curated gold set" names the
exact blocker instead of hiding behind "TBD." Hedging would be vague qualifiers; this is closer to an
audit trail. My one reservation: it never asks what to do about the gaps, no ranked recommendation on
what to build or measure next.

**3. Executive-ready vs needs a rewrite.** Ready: "Roll back when P95 latency exceeds 200ms, or
recall drops below 90%." (sourced to `rollback.sql`), concrete, decision-encoded, no jargon tax.
Needs a rewrite: "The graph vat is Postgres with pgvector. Entities are rows, edges are an adjacency
list keyed by strength, and the system stores a relational table, not a graph database." That's
implementation detail wearing an executive-summary font size. No exec needs to know it's
rows-not-a-graph-database unless it's costing something.

**4. Showing off vs communicating.** The "24 Hour Atomize AI News Cycle" radial clock dial with a
draggable needle. It's a genuinely nice interaction, but it re-explains one idea already stated in
prose two sentences earlier (cron-driven vs queue-driven). The visualization outweighs the point it's
making.

**5. Unanswered question.** Every disclosed gap (spaCy check unwired, HNSW rollback never tested, RRF
quality unmeasured) is presented as observation, not prioritized. I'd need to ask: of these five
"built not wired" items, which one would you actually spend the next sprint on, and why that one
first?

**6. Score.** 7/10. Real epistemic honesty and one genuine tradeoff decision earn it well above
average, but it's an inventory of a system dressed as strategic communication. It shows what the
candidate audited, not what they'd do about it.

---

## P3. PhD AI researcher
Works on retrieval and knowledge graphs. Reviews papers. Skeptical by default.

**1. Judgeable, within limits.** This is deeper than a marketing page but shallower than a paper: no
ablations, no held-out eval set, most claims are architecture description, not results. The deepest
checkable claim is the Intent Cascade routing entry: "Turning this on lets a three-tier classifier
change which retrieval strategy runs for a query." Quality: "28 better, 4 worse, 13 neutral. Source:
commit 36df9d062, differential run, 64 live queries." Blast radius: "45 of 64 queries retrieve
differently, 70.3%. This size is the stated reason the flag stays off." That's a real differential
test with a commit hash and an honest reason for not shipping it, the one place the page reports a
negative-leaning result and explains inaction.

**2. The taxonomy is real, not decoration.** Legend: MEASURED "a number was actually recorded,"
REASONED "a written rationale exists in the repository," INFERRED "we read the reason from the code,
nobody stated it," DEFAULT "a library or bare constant nobody tuned," BUILT NOT WIRED, NO RECORD.
It's applied with discipline: all 9 Acquire-stage components are INFERRED (not MEASURED), and every
"BUILT NOT WIRED" feature (Orchestrator V2/RRF, Intent Cascade, spaCy direction check, HNSW rollback)
correctly carries no performance claim beyond what was actually run. I found no mislabeled badge. One
thing worth flagging: "Quality... This axis was never measured" for Orchestrator V2 sits right next to
hard latency numbers (92ms to 2146ms cold, ~0ms warm). The pairing invites you to read speed as
validation when correctness was never checked.

**3. Design choice I'd challenge.** "Neighborhood traversal is done as plain sequential queries, not
one recursive query" (Graph Explorer, INFERRED). Sequential per-hop fetches instead of a single
recursive CTE is an N+1 pattern. It'll degrade non-linearly as neighborhood fan-out grows, and
Postgres-as-graph-store already forgoes native traversal. I'd want to see the fan-out ceiling before
calling this "fine."

**4. Under-supported claim.** "Sixteen Vercel cron routes fire through the UTC day... each one a real
route in the codebase. Six Railway workers stay lit the whole time." I can't check the codebase, so
the "sixteen" and "six" are asserted, not shown: no route listing, no repo link.

**5. Wasted time.** The inline glossary tooltips: "pgvector is a Postgres extension that stores
vectors as a native column type," "a reranker takes the shortlist a search returned and reorders it,"
"vector search finds passages by meaning rather than by matching words." Baseline retrieval
definitions a reviewer doesn't need; they dilute the real content.

**6. Real result or dressed-up documentation.** There's a real result, but a narrow one. The Intent
Cascade differential (28/4/13 over 64 queries, kept off due to blast radius) and the reject-code
accounting (component counts sum exactly to the reported rejected-facts total) are genuine, checkable
engineering artifacts. Everything else is architecture documentation with unusually honest epistemic
labeling: not evidence of system quality, but not dressed-up marketing either. It's a transparent
build log, not a paper.

---

## P4. Complete AI novice
No technical background. Has used a chatbot a few times. Friend sent the link saying "this is what I built."

**1. Could I explain this to a friend?** Not really. The closest I could manage: "It's some kind of
demo where a computer program reads news articles and only keeps facts it can prove with an exact
quote, and you can turn switches on and off to see what breaks." I could not tell you what it's
actually FOR, who would use it, or why I'd want it.

**2. First thing that confused me.** "PIPELINE UNIT 01, A WORKING SCALE MODEL" right under the title,
before I even knew what "it" was. Close second, a few seconds later: "CONTENT_QUALITY_FLOOR" printed
as a raw code variable name directly under a plain-English toggle called "Quality Floor." I don't know
what that string means or why I'm being shown it.

**3. Genuinely surprising.** The little live diagram near the bottom (dots labeled "GRAPH VAT"
connecting with lines, a "query" dot sliding toward them) actually moved and changed numbers when I
clicked buttons. That felt like a real machine responding, which none of the text above it did.

**4. Where I gave up.** The "WHAT-IF LEVERS" section, specifically the item "Roll back HNSW to
IVFFlat" with text like "The service configures a batch size of 50 and a single worker
(spacy-service/railway.toml)" and "Roll back when P95 latency exceeds 200ms." I stopped trying to
understand anything after that. It reads like an internal engineering changelog, not something
written for a visitor.

**5. Did clicking help?** Yes, I noticed I could click things, and clicking did do something. Buttons
like "FEED ONE ARTICLE" changed numbers and the diagram at the bottom. But it never told me what the
numbers meant in a way I could use ("13 FACTS KEPT," kept from what, is that good?). So clicking
proved the thing was "real" but didn't teach me anything.

**6. How it made me feel about the builder.** Impressed that they clearly know what they're doing
(the level of technical specificity is real, not fake), but excluded. This reads like it was written
for another engineer to audit, not for a friend to understand. I'd say "looks impressive, I have no
idea what it does."

---

## P5. AI lab product lead
Ships retrieval and agent products. Has seen a hundred architecture diagrams, most of them decoration.

**1. Does the interactive part teach anything a static diagram would not?** Yes. Toggling "Search
Orchestrator V2" showed cold-path latency jump from 92ms to 2146ms (23x) with a "warm, cached to ~0ms"
line. I wouldn't have grasped that this feature's cost is a one-time cache-fill spike, not a steady
tax, from a diagram. Toggling "Intent Cascade routing" surfaced a live A/B readout: 28 better / 4
worse / 13 neutral across 64 queries, but 45 of 64 (70.3%) retrieve differently, and the panel states
outright that blast-radius size, not the net-positive result, is why the flag stays off. That's a
genuine engineering trade-off exposed by manipulation, not narration.

**2. Built-and-never-shipped features: real judgment or excuse?** Real judgment. What sells it: the
page distinguishes measured (the RRF fusion latency numbers, the cascade A/B) from reasoned
(chunk-sizing rationale) from unmeasured-and-says-so (spaCy check: "This axis is unmeasured. No
latency or accuracy figure exists," then gives a structural argument, batch size 50, single worker,
config file cited, instead of faking a number). Citing actual commit hashes and a real rollback
trigger tied to a migration file is the kind of detail nobody fabricates for a demo. It reads as
someone who has actually shelved a feature and can state the number that would unshelve it.

**3. Controls touched, and whether the effect was legible.** Touched: WHAT-IF mode toggle, Grounding
strictness slider (drag didn't register via keyboard, but direct value-set worked), Search
Orchestrator V2, Intent Cascade routing, spaCy direction check, Roll back HNSW to IVFFlat, FEED ONE
ARTICLE, RUN A QUERY, the BLUEPRINTS tab plus a stage-detail expansion. All had a visible consequence:
counters moved, reject-reason tally updated live, panels grew consequence data. One control I could
NOT perceive an effect from: RUN A QUERY. QUERIES SERVED stayed at 0 in one observation despite
clicking it while facts existed. I didn't chase down whether that's a timing gate or a real dead click.

**4. What's missing that a production operator would expect.** No cost or error-budget framing tied
to the "$0.00 downstream AI spend" counter; a real operator wants to see what that number does under
10x load, not at idle. No on-call or alerting path for the stated rollback trigger (P95>200ms); a
documented threshold with no owner is half a runbook. No discussion of what happens to in-flight
facts when Gate Power is flipped off mid-run. The graph-trust metric is a single scalar with no
decomposition of what's dragging it down when levers move.

**5. Where the page wastes time.** The tooltip-glossary buttons are the kind of decoration I'd cut in
review: fine for a public explainer, dead weight for the audience this is clearly built for. Also,
scrolling through five source-hopper checkboxes that all say functionally the same sentence is
repeated filler; one hopper explained plus a compact table would say the same thing in a third of the
scroll.

**6. Would you interview this person?** Yes. The honesty taxonomy applied consistently across dozens
of components, plus citing real commit hashes and a real rollback SQL migration for a documented
threshold, is not something people fake. It's what someone who has actually operated a system under
uncertainty and had to justify a "no" produces.

**Caveat, marked honestly.** On mobile (390x844) the header's "BLUEPRINTS" tab is clipped to "BLU" at
the right edge, a real uncaught reflow bug on the primary nav.

---

## P6. AI-native learner
Self-taught builder, twenties. Ships small apps, uses AI daily, never built a retrieval pipeline.

**1. Did you learn, or just enjoy the visuals?** Mostly the second, but I did learn one real thing: I
now get why a fact gets rejected instead of just "the AI messed up." When I hit Feed One Article, the
reject counters ticked up with actual reason codes, "quote not grounded," "confidence < 0.5," not a
vague error. So a rejection is a specific check failing, not a vibe.

**2. The moment it clicked.** The Blueprints tab, top legend: MEASURED / REASONED / INFERRED /
DEFAULT / BUILT NOT WIRED / NO RECORD, each tagging where a number came from. That's when it clicked
that most of this dashboard is honesty-labeling, not a feature demo. It's telling you which numbers
are real and which are decoration. Before that I thought the whole thing was "live."

**3. The jargon wall.** "Reciprocal Rank Fusion at k=60" lost me completely, and so did "P95 latency
exceeds 200ms." I did notice the underlined terms and clicked a couple. Those popovers actually
helped a lot, plain English plus a "how it works" paragraph. But I skimmed most of the What-If Levers
section: too many acronyms stacked at once, I stopped reading carefully after "roll back HNSW to
IVFFlat."

**4. Phone annoyances.** The sliders (Grounding strictness, Edge strength floor) would not budge with
taps or arrow keys on the phone, dead ends. Also everything is one long vertical scroll; I scrolled
past the same panel five or six times hunting for "Feed One Article," and the pipeline diagram up top
got cut off sideways so I couldn't see the whole Acquire to Surface flow at once. Desktop fixed both:
two columns, sliders workable, full diagram visible.

**5. What I wanted that isn't here.** A single "show me one fact's whole journey" trace. Pick one
article, watch it move hopper to gate to graph to answer, instead of me inferring that from separate
counters.

**6. Would you send it to a friend who is learning?** Yes. The honesty about what's fake ("SIM ONLY,"
"BUILT NOT WIRED," never-run RAGAS) is rare and worth showing a friend, even with the jargon walls.
