# Round two, six personas, and what survived checking

Six reviewers read a frozen snapshot: technical recruiter, strategy hiring manager,
PhD AI researcher, complete AI novice, AI lab product lead, AI-native learner. Each
was blind to round one and to the others. Raw reports sit beside this file.

Every claim below was checked against the page rather than accepted. The split
matters more than the count: **the reviewers were strongest on reading and weakest on
tooling**, and their tooling failures were confident and specific enough to look like
findings.

## Confirmed and fixed

**Nine of 22 job labels rendered NaN.** Found by the recruiter, who saw three. Three
are hourly crons whose hour field is a bare star, and the formatter did `+'*'`. The
other six are not clock-driven at all: their schedule reads `queue event` or
`http service`, and forcing that through a cron parser printed `daily at NaN:NaN UTC`
against exactly the Railway workers that section exists to contrast with cron routes.
The bug contradicted the section's own teaching point. `build.py` now renders all 22
labels and refuses a build that would print a NaN.

**The page had no viewport meta and no charset.** Found by the researcher. Inside the
artifact wrapper the page inherits both, which is why it never showed. Opened as a
file, served without a charset, or dropped into another site, a phone lays the page
out near 980px and every breakpoint below that never fires. The entire mobile layout
was dead code outside one hosting path. Both declared, both gated.

**The hidden attribute was not authoritative.** Found by the product lead. Three class
rules set `display`, and a class beats the user agent's `[hidden]` rule, so lock
notes, consequence panels and the mode reminder stayed on screen after the code hid
them. In What-if mode that put controls-unlocked and a padlock-still-locked line on
one screen. Fixed globally in the shell and gated. Worth noting that the control
probe had been reading the attribute back rather than the computed style, so the
instrument agreed with the bug.

**NO RECORD overclaimed.** Found by the researcher. 41 of 48 component badges are
derived rather than authored, and the derived NO RECORD branch shipped with no note
while its legend told the reader no rationale exists in the repository. Nobody
searched the repository. It now states its real basis.

**Four canvas annotations dropped their mechanism on phones.** Found by the learner
and the product lead independently. A desktop reader got
`dedupe, SHA-256(title,link,date-bucket), SSRF guard`; a phone reader got `dedupe`.
They now take the longest form that measures within the space available.

**Run a query looked dead for six seconds** because the counter moves when the query
lands. The status line now says so at the moment of the click.

**View tabs measured 33px on a phone**, under the 44px floor the rest of the page
honours. Raised.

## Checked and refuted

**"The controls are dead."** Three reviewers, one naming all 10 reject-reason tiles,
all 9 counter tiles and the 5 blueprints stage cards. `check-controls.html` clicks
each and diffs the state it should change: **15 of 15 live, none dead.** All three
leaned on a structural scan that cannot see handlers attached by delegation and that
captures before the view router turns a view on, so it reads a hidden view's controls
as absent.

**"Clicking BLUEPRINTS renders five empty strips, content absent from the a11y tree."**
Five cards render with 142 to 184 characters of text each, via the tab click.

**"r-intent is badged MEASURED on FLOOR and BUILT NOT WIRED on BLUEPRINTS."** There is
no intent badge on FLOOR. The MEASURED badge there sits on the cascade evidence, which
was measured, while the component that would ship it is correctly BUILT NOT WIRED.
Two true statements about different things.

**"The status says paused while counters climb."** The sentence already says
"Feed one article or run a query still applies at once." The reviewer read the first
clause. The sentence may be too long to survive a skim, but nothing is wrong.

## The instrument, again

Two of six reviewers were fighting the test server, which was single-threaded: six
agents loading a 310KB page queued until requests timed out, which reads exactly like
a page that will not load. It is threaded now, six concurrent requests at 27ms each.
That flaw plausibly corrupted parts of every session, so tooling-dependent claims from
this round carry less weight than reading claims.

Round three should give each reviewer its own server port, or serve statically.

## Open, and not mine to decide

1. **The novice did not understand it past two sentences** and counted about 50
   unexplained terms, saying the glossary "moved the confusion one layer down" by
   defining jargon with jargon. Either the page keeps a complete novice as an audience
   and the glossary is rewritten to bottom out in plain language, or that audience is
   dropped on purpose. It cannot stay as it is and claim both readers.
2. **The product lead wants the thesis reordered**: lead with the cascade decision,
   make the provenance taxonomy the argument, and demote the machine to an appendix.
   Four of six reviewers named the taxonomy as the reason to trust the work, and two
   said the factory is table stakes. That is a real signal, and a large restructure.
3. **MEASURED appears on zero of the 48 component cards.** Six badge classes are
   advertised and four are reachable. Extending the seven authored badges is a content
   decision.
4. **The hiring manager reads the H1 as marketing fog** that the honest subhead
   immediately contradicts. One-line change, but it is a voice decision.
5. **The researcher's single ask needs the live system**, not this repo: recall@50
   against exact kNN on the index that actually serves, published with the row count.
   It would settle the two-lineage conflict the page names and never resolves, and
   would populate MEASURED once.
