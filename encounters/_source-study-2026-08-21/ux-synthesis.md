# The Fact Refinery, usability synthesis

Study object: `eval-snapshot.html`, six participants, phone (390x844) and desktop (1440x900).
Researcher observation conducted independently on 2026-08-21 against the live page at
`http://127.0.0.1:8800/eval-snapshot.html`, plus a source read of the served HTML.

---

## 1. Headline finding

The page succeeds at the hard thing it set out to do and fails at the easy one. Its provenance
taxonomy is the rarest asset on the page, and four of six participants independently identified it
as the reason to trust the builder rather than as decoration. What defeats participants is not the
dual-audience bet, it is navigation and feedback. Three of the four controls that participants
called broken are not broken at all: they are gated, and the gate is silent. The single strongest
piece of evidence on the entire page, the Intent Cascade differential, is buried inside the exact
section that three participants told me to skip or delete. The page is therefore not too technical
and not too simple. It is unlabelled. Almost every serious problem found here is a missing sentence
telling the visitor what state they are in, not a missing feature and not a wrong audience.

---

## 2. What works, and the evidence

Only findings that two or more participants reached independently are listed.

**The provenance taxonomy is the page's strongest asset. Four participants.**
P2 called it "a provenance system, not a disclaimer" and contrasted it with hedging: "Hedging would
be vague qualifiers; this is closer to an audit trail." P3 audited it and reported "It's applied
with discipline... I found no mislabeled badge." P5 said "The honesty taxonomy applied consistently
across dozens of components... is not something people fake." P6 named the legend as the moment
the page clicked: "That's when it clicked that most of this dashboard is honesty-labeling, not a
feature demo." Note that P2, P3 and P5 arrived at this from three different professional motives,
which makes the convergence stronger than the count alone suggests.

**The Intent Cascade differential is the single most persuasive artifact. Three participants.**
P2: "That's a candidate choosing not to ship a net-positive change because blast radius was too
large to trust, a real tradeoff, with the number that drove it." P3 called it "the deepest checkable
claim" and "the one place the page reports a negative-leaning result and explains inaction." P5:
"That's a genuine engineering trade-off exposed by manipulation, not narration." All three named the
same numbers unprompted: 28 better, 4 worse, 13 neutral, 45 of 64 at 70.3%.

**Interactivity proves the system is real in a way static text did not. Four participants.**
P1: "That's not a mockup, that's a running counter reacting to my clicks." P4, who understood least,
still reported the diagram "actually moved and changed numbers when I clicked buttons. That felt
like a real machine responding, which none of the text above it did." P5 said toggling taught him
something a diagram would not have: the cost of Orchestrator V2 "is a one-time cache-fill spike,
not a steady tax." P6 confirmed the same mechanism from the novice end.

**Reject reason codes teach a specific, transferable idea. Two participants.**
P6 stated the lesson explicitly: "a rejection is a specific check failing, not a vibe." P1
independently singled out the same breakdown, "10 quote not grounded, 4 confidence < 0.5," as
evidence of real measurement. This is the one concept that landed across the expertise gap.

**Commit hashes and cited config files read as non-fabricated. Two participants.**
P5: "Citing actual commit hashes and a real rollback trigger tied to a migration file is the kind of
detail nobody fabricates for a demo." P2 independently cited the same quality, naming commit
52d7ee93f as an example of naming "the exact blocker instead of hiding behind TBD."

---

## 3. What fails, ranked by severity

### Confirmed defects

These are cases where a control genuinely does not do what a reasonable visitor expects. I verified
each one myself.

**D1. RUN A QUERY silently does nothing when the graph holds fewer than five nodes. Severity: high.**
P5 reported it: "One control I could NOT perceive an effect from: RUN A QUERY. QUERIES SERVED stayed
at 0 in one observation despite clicking it while facts existed." P1 hit the phone version of the
same thing. P5 was correct to suspect a gate and correct not to call it a dead click. The served
source contains the cause: `function runQuery(instant){ if(nodes.length<5) return; ... }`. The guard
returns with no toast, no disabled state, no explanatory text and no visual change of any kind. Cost:
this is the control most likely to be clicked by a visitor who wants to see the retrieval half of the
system, and it is the one most likely to do nothing. P5 still recommended an interview despite it,
so it did not sink the page, but it silently removes the payoff from the pipeline's second half.

**D2. The simulation loop pauses whenever the machine canvas is scrolled out of view. Severity: high.**
P1 reported the symptom precisely: "I tapped FEED ONE ARTICLE and RUN A QUERY and nothing visibly
happened on my screen. The counters that changed were several scrolls away, so it felt broken until
I scrolled up." The source confirms an `IntersectionObserver` at `threshold:.02` that sets `visible`,
and the animation loop runs only under `if(visible && !REDUCED && !document.hidden)`. My own desktop
session corroborates it: every counter read zero for the entire session, including ARTICLES FED,
while AUTO-FEED displayed ON. The gate is a defensible performance decision. Its interaction cost is
not defensible, because on phone the single column separates the buttons from the canvas they drive.
This compounds D1: with the loop paused, no nodes are ever created, so RUN A QUERY can never pass its
own precondition. Cost: on phone these two defects together make the page's core interactive claim
unreachable, and the interactivity is what three participants called its best feature.

**D3. The BLUEPRINTS nav tab is clipped to "BLU" on phone. Severity: medium.**
P1 and P5 reported this independently. P5 flagged it as "a real uncaught reflow bug on the primary
nav." I reproduced it at 390x844 on first paint. Cost: this is the entry point to the second view,
and P6 reported that the second view contains the legend that made the whole page make sense. A
clipped label on the control leading to your best explanatory asset is worse than it looks.

**D4. Long source paths and the pipeline diagram clip horizontally on phone. Severity: medium.**
P1: source text like "prisma/migrations/20251013000653_upgrade_to_hnsw_inde..." runs off the right
edge. P6 independently reported "the pipeline diagram up top got cut off sideways so I couldn't see
the whole Acquire to Surface flow at once." Two participants, two different elements, same root
cause. I confirmed the narrow-viewport layout but did not measure each clipped element individually,
so treat the specific elements as participant-reported and the class as confirmed.

### Design problems

These work as built. They confuse anyway.

**DP1. The sliders are disabled by default, and nothing adequately says so. Severity: high.**
This is the most consequential reframe in the study, because two participants reported it as a
broken control and it is not one. P6: the sliders "would not budge with taps or arrow keys on the
phone, dead ends." P5: "drag didn't register via keyboard, but direct value-set worked." Both
reports have a single cause. The page initialises with `setMode('real')`, which runs
`LOCK_IDS.forEach(function(id){ var el=$(id); el.disabled=isReal; ... })`. The sliders carry the HTML
`disabled` attribute on load. I verified the behaviour directly: in REAL SETTINGS mode the Grounding
strictness slider renders grey and does not respond, and one click on the WHAT-IF mode button turns
both sliders amber and makes them live.

Two participant claims need correcting against this. P6 believed the viewport was the variable:
"Desktop fixed both: two columns, sliders workable." P6 was mistaken about the cause. Desktop does
not unlock the sliders. What desktop does is place the MODE switch in the same viewport as the
slider it governs, so P6 almost certainly clicked WHAT-IF on desktop without registering it as the
unlock. On phone that switch scrolls away from the control it governs. P5's observation that "direct
value-set worked" while user input did not is the exact signature of a `disabled` input, since
programmatic assignment bypasses the disabled state and human interaction does not. P5 was reading
the symptom accurately and had no way to see the cause.

The page does show a lock note reading "Locked at 1.0, fully strict." It is rendered in low-contrast
grey beneath the control, and it did not prevent either participant from concluding the page was
broken. Cost: the page's central invitation is "Operate the gates below, close a hopper, or loosen a
threshold." Two of six participants tried exactly that, failed, and concluded the page was buggy
rather than locked.

**DP2. The WHAT-IF LEVERS section stops readers. Three participants. Severity: high.**
This is the highest-frequency complaint in the study. P1: "That whole middle section reads like it's
written for another engineer reviewing his PR." P4 quit there permanently: "I stopped trying to
understand anything after that," and confirmed in follow-up that "That's where I stopped reading and
never came back." P6 skimmed it: "too many acronyms stacked at once, I stopped reading carefully
after roll back HNSW to IVFFlat." Three participants named the same trigger terms: Reciprocal Rank
Fusion at k=60, HNSW to IVFFlat, P95 latency. Cost is severe and it is compounded by placement,
which section 4 addresses: the page's best evidence lives inside its least readable section.

**DP3. The page never says what the system is for or who would use it. Two participants. Severity: high.**
P4 could not answer the basic question: "I could not tell you what it's actually FOR, who would use
it, or why I'd want it." P1 hit a milder version: "I couldn't tell what he actually built until I
scrolled several screens down." The page does open with a purpose line, "Atomize reads the day's AI
news and research, then keeps only the facts it can prove with a verbatim quote," which I confirmed
on screen. That sentence says what the system does. Neither participant's question was what it does.
Both asked who it is for and why it exists. P4 also flagged that the line above it,
"PIPELINE UNIT 01, A WORKING SCALE MODEL," arrives "before I even knew what it was."

**DP4. Numbers appear without any reference frame. Two participants. Severity: medium.**
P4: "it never told me what the numbers meant in a way I could use (13 FACTS KEPT, kept from what, is
that good?)." P5 reached a related conclusion from the opposite end, wanting the $0.00 spend counter
framed against load and calling graph trust "a single scalar with no decomposition of what's dragging
it down when levers move." These are not the same request. P4 wants a baseline that says whether a
number is good. P5 wants a breakdown that says what moved it. Both are the same underlying gap: the
page reports magnitudes without scales.

**DP5. Five hopper checkboxes repeat one identical sentence. Two participants. Severity: medium.**
P1 counted it: the sentence "Closing this valve seals the hopper. No new articles fall from it until
you open it again" appears five times back to back. P5 independently called it "repeated filler" and
proposed the fix: "one hopper explained plus a compact table would say the same thing in a third of
the scroll." I confirmed all five instances, visible in two screens at desktop width. Cost is
scroll-tax rather than comprehension, but it lands in the first third of the page where attention is
most valuable.

**DP6. The page presents an audit, not a decision. One participant, strongly. Severity: medium.**
P2 is the clean source and was unambiguous: "Everything else on the page is inventory (a labeled list
of what exists), not a decision (why one thing was chosen over another)," and the closing verdict,
"It shows what the candidate audited, not what they'd do about it." P2 named the specific missing
move: "of these five built not wired items, which one would you actually spend the next sprint on,
and why that one first?" P3 and P5 reached adjacent conclusions from other directions. P3 called the
page "a transparent build log, not a paper." P5 noted "a documented threshold with no owner is half a
runbook." I am counting this as one primary source with two corroborating observations, not three.

**DP7. A never-measured quality axis sits beside hard latency numbers. One participant. Severity: medium.**
P3 alone caught this, and it is the most technically serious single observation in the study: "Quality
... This axis was never measured for Orchestrator V2 sits right next to hard latency numbers (92ms to
2146ms cold, ~0ms warm). The pairing invites you to read speed as validation when correctness was
never checked." I confirmed the layout. The SPEED bars and the italic line "This axis was never
measured" render in one continuous panel with no separation. The page's own honesty system is what
makes this dangerous: a visitor who has learned to trust the badges may read the panel as validated.

**DP8. Raw environment variable names sit under plain-English labels. One participant. Severity: low.**
P4: "CONTENT_QUALITY_FLOOR printed as a raw code variable name directly under a plain-English toggle
called Quality Floor. I don't know what that string means or why I'm being shown it." Confirmed on
screen. For the expert audience these strings are the page's proof of realism, so this one is a
genuine dual-audience cost rather than a simple error.

---

## 4. Where participants disagreed, and my call

### The glossary tooltips

The split is clean and both sides were emphatic. P4 and P6 found them the most useful element on the
page. P6: "Those popovers actually helped a lot, plain English plus a how it works paragraph." P3 and
P5 wanted them gone. P3: "Baseline retrieval definitions a reviewer doesn't need; they dilute the
real content." P5: "the kind of decoration I'd cut in review: fine for a public explainer, dead
weight for the audience this is clearly built for."

**My call: keep them, default them on, and cut their visual weight. Do not make them opt-in.**

The obvious compromise, hiding them behind a switch, is foreclosed by evidence. I put it to P4
directly and the answer was unambiguous: "I'd never find it. I wasn't hunting for a settings panel, I
was just reading top to bottom. Opt-in and tucked away is functionally the same as not existing for
me. It would need to default ON to actually help." An opt-in glossary is a glossary that serves
nobody, because the people who would enable it are the people who already know the terms.

The novice need is load-bearing and the expert objection is not, for a reason visible in the raw
transcripts. Neither P3 nor P5 let the tooltips change their verdict. P5 recommended an interview.
P3 delivered a considered technical assessment. The tooltips cost them scroll and mild irritation,
and both filed the complaint under wasted time rather than under damage. For P4 and P6 the tooltips
were the difference between reading and not reading. That asymmetry decides it: a preference cost to
the expert does not outweigh a comprehension benefit to the novice.

The wording of the expert objection also points at the remedy. P5 did not say the definitions are
wrong, but that they are "fine for a public explainer," which concedes the content has a legitimate
audience and locates the objection in audience-fit. P3's word was "dilute," which is about density
in the reading path. Neither objection is to the definitions existing. Both are to their weight on
the page. Current treatment renders them as interactive buttons with underlines, which is why they
read as page furniture to an expert scanning for evidence. Rendering them as a subtle dotted
affordance with no button chrome, still default-on and still clickable, addresses the stated
objection at its stated cause.

I should mark the limit on this one honestly. I have P4's follow-up but not P3's or P5's, so my read
of their objection as weight-based rather than existence-based is inference from their raw wording,
not something either confirmed. If either would accept nothing short of removal, my recommendation
still stands, because the novice's need is the one that changes whether the page works at all.

### Whether to cut the WHAT-IF LEVERS section

Participants effectively disagreed with themselves here, and it is worth naming plainly rather than
averaging. P1 said skip it. P4 said "I wouldn't miss it. The page would be better for me without it."
But P3, P5 and P2 all drew their single most positive judgement from the Intent Cascade panel, which
sits inside that section. Deleting the section would destroy the page's best evidence to spare its
weakest readers.

**My call: promote the Intent Cascade panel out of the section, then collapse what remains.** This is
not a split-the-difference answer, it is the only move that serves both. P4 volunteered the same
structure unprompted: "If a technical audience needs it, hide it behind disclosure rather than
delete it, but for me, removing it loses nothing."

### A participant who was mistaken

P6 reported that desktop fixed the sliders. My observation contradicts this. The sliders are gated by
mode, not by viewport, and desktop does not unlock them. P6 almost certainly clicked the WHAT-IF mode
switch on desktop without registering it as the unlock, because on desktop it sits in the same
viewport as the slider. The finding survives the correction and gets sharper: the defect is the
distance between the mode switch and the control it governs, not the viewport.

---

## 5. Audience-by-audience verdict

**Technical recruiter. Partly.** She got the two sentences she needed and would forward the page,
but only with a warning attached, and she said the middle third "would make a non-technical hiring
manager bounce" on its own. The one change: collapse the levers section behind disclosure so the
page can be forwarded without a chaperone.

**Strategy hiring manager. Partly.** Scored it 7/10 and found real epistemic honesty plus one
genuine tradeoff, but judged it "an inventory of a system dressed as strategic communication." The
one change: add the ranked next-sprint recommendation he explicitly asked for.

**PhD AI researcher. Partly.** He could judge it and found no mislabeled badge, which is a real pass
on the page's own terms, but concluded it is "a transparent build log, not a paper." That is a fair
verdict for what the page is rather than a failure. The one change: make the asserted counts, sixteen
cron routes and six workers, checkable rather than asserted.

**Complete AI novice. No.** She could not say what the system is for, who would use it, or why she
would want it, and she quit permanently at the levers section. She was left feeling "excluded." The
one change: the purpose sentence at the top, in her words, "This is a demo of the part of our news
tool that checks facts before they get used, built so you can see exactly what it keeps and what it
throws away, and why."

**AI lab product lead. Yes.** He would interview the builder, and he was the only participant who got
the full intended payoff from the interactive levers. He hit the RUN A QUERY defect and it did not
change his verdict. The one change: fix the silent no-op on RUN A QUERY, which is the one control
that failed to teach him anything.

**AI-native learner. Partly.** He learned one real transferable idea, that a rejection is a specific
check failing, but reported he "mostly" just enjoyed the visuals. The one change: move the provenance
legend onto the first view, since he identified reaching it as the moment the page made sense and it
currently sits behind a clipped nav tab.

---

## 6. Ranked recommendations

Ordered by evidence strength multiplied by impact, not by ease.

**1. Fix the three confirmed phone defects: the silent RUN A QUERY guard, the visibility-gated
simulation loop, and the clipped BLUEPRINTS tab.**
Evidence: P1 and P5 on the dead controls, P1 and P5 on the clipped nav, plus my own reproduction and
source read of all three. Expected effect: the page's most-praised quality, that the interactivity
proves the system is real, currently fails on phone for the visitors most likely to arrive there.
Give RUN A QUERY a disabled state or an inline line reading that it needs facts in the graph first,
and let the loop run briefly when its controls are on screen even if the canvas is not. Cost: small,
and localised to three places in one file.

**2. Add a purpose sentence naming who the system is for, directly under the title, above any factory
metaphor.**
Evidence: P4 could not state the purpose at all, P1 could not find it for several screens. P4 drafted
the sentence herself in follow-up. Expected effect: this is the single change that moves the novice
from no to partly, and it costs the expert audience nothing. Cost: one sentence, plus moving
"PIPELINE UNIT 01, A WORKING SCALE MODEL" below it.

**3. Make the REAL SETTINGS lock legible at the control, and keep the mode switch adjacent to the
controls it governs on narrow viewports.**
Evidence: P5 and P6 both concluded a working control was broken. Expected effect: removes the study's
only false broken-control impression, which two of six participants formed. The existing grey lock
note is insufficient. Put the lock state on the slider itself and let a click on a locked control
reveal the unlock rather than doing nothing. Cost: small, and no logic change is required.

**4. Promote the Intent Cascade panel to the top of the page, then collapse the remaining levers
behind disclosure.**
Evidence: P2, P3 and P5 independently named this panel as the page's best artifact. P1, P4 and P6
independently bounced off the section containing it. P4 endorsed disclosure over deletion. Expected
effect: the strongest evidence stops being gated behind the weakest reading experience. P2 said this
item alone earns the page its score, and it is currently buried. Cost: medium, since it means
restructuring the section. This is the highest-value structural change on the list.
**Cross-audience conflict: none, and that is the point.** Deletion would harm experts, and leaving it
alone harms everyone else. Promotion plus disclosure is the only option that harms neither.

**5. Give every headline counter a reference frame.**
Evidence: P4 could not tell whether 13 FACTS KEPT was good news, and P5 wanted the trust scalar
decomposed and the spend counter framed against load. Expected effect: converts the counters from
proof-of-life into information. P4's own formulation is the model: a number, a percentage, and a
normal range. Cost: medium, because a defensible normal range has to be derived rather than invented,
and inventing one would violate the page's own provenance standard.

**6. Keep the glossary default-on and cut its visual weight.**
Evidence: P4 and P6 found it the most useful element, P3 and P5 called it dead weight, and P4 killed
the opt-in compromise explicitly in follow-up. Expected effect: preserves the comprehension benefit
that gets two participants through the page while removing the scanning cost the other two named.
Cost: small, a styling change only.
**Cross-audience conflict: yes, and it cannot be fully dissolved.** The expert keeps a small residual
cost. I am accepting that deliberately, because the novice's need is comprehension and the expert's
is preference, and because neither expert let the tooltips change their verdict.

**7. Add a ranked next-sprint recommendation over the disclosed gaps.**
Evidence: P2 asked for exactly this and named it as the gap between 7/10 and higher. P3 and P5 made
adjacent observations about unprioritised gaps and ownerless thresholds. Expected effect: converts
the page from audit to decision for the audience that hires on judgement. Cost: small to build, but
it requires the builder to commit to a ranking in public, which is the actual cost.
**Cross-audience conflict: mild.** This adds length to a page three participants already found too
long. Placing it as a short ranked list near the top rather than as another section mitigates it.

**8. Collapse the five hopper checkboxes to one explained hopper plus a compact table.**
Evidence: P1 counted five identical sentences and P5 independently proposed this exact remedy.
Expected effect: recovers roughly two phone screens of scroll in the first third of the page, where
P1 was still deciding whether to keep reading. Cost: small.

Two findings are deliberately excluded from this list for lack of corroboration, and both deserve
attention anyway. P3's observation that Orchestrator V2's unmeasured quality axis sits beside hard
latency numbers is the most technically serious single-source finding in the study, and it is a
credibility risk precisely because the page's badges have earned trust. P3's N+1 concern about
sequential neighborhood traversal is an engineering question this study cannot adjudicate.

---

## 7. What this study cannot tell you

**Five of six follow-up interviews did not happen.** This is the most important limit and it is not a
minor one. Only the complete AI novice remained reachable. The other five sessions had been reaped
and could not be resumed, so every question I prepared for the recruiter, the strategy manager, the
researcher, the product lead and the learner went unasked. Their positions in this report come
entirely from their original transcripts.

**That creates a specific bias risk in section 4.** The novice is the only participant who got a
second turn, and her follow-up is load-bearing in my glossary recommendation. I have tried to hold
her answer to its actual weight, one participant answering one question, and to rest the
recommendation on the asymmetry visible in all four raw transcripts rather than on her follow-up
alone. A reader who discounts her follow-up entirely should still reach the same call, but should
hold it less firmly. My characterisation of what P3 and P5 would accept is inference from their
wording, and neither confirmed it.

**I declined an offer to re-run the five as reconstructed participants.** A reconstructed persona
given its own prior report and asked to elaborate is liable to rationalise a position it never held,
which would have produced quotable material of unknown validity. For the two dead-control questions
the browser was the better instrument anyway, and it settled both.

**Six participants, simulated rather than recruited.** These are constructed personas, not sampled
humans. They cannot tell you the base rate at which real visitors bounce, and the convergence of four
participants on the provenance taxonomy may partly reflect shared construction rather than
independent discovery.

**No task success metrics and no timing data.** Nobody was given a task to complete or fail, so
statements like "P4 gave up" are self-reported, not measured. I have no time-on-page, no scroll
depth, and no data on how long anyone persisted before disengaging. Every severity rating in section
3 is my judgement informed by participant count, not a measured cost.

**One session each, with no repeat exposure.** First-run confusion and durable confusion are
indistinguishable here. The mode-lock problem in particular may vanish on a second visit, which would
change its severity considerably.

**My own verification used headless Chrome, not a touch device.** I confirmed the mode-lock mechanism
in source and in a desktop browser, which explains both slider reports. I did not confirm the
phone-specific touch behaviour on real hardware, so if a separate touch-only defect exists on top of
the mode lock, this study would not have found it. The clipped nav and clipped source paths were
confirmed at a 390px viewport, which is a reasonable proxy but not a real phone.

**The study says nothing about whether the system works.** Every participant judged a page about a
pipeline. P3 was explicit that the page's claims are mostly architecture description rather than
results, and that he could not check the codebase. Nothing here validates Atomize AI itself.
