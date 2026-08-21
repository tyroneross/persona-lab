# P4 — Complete Novice Review of "The Fact Refinery" (eval-snapshot.html)

I looked at this using screenshots and by clicking/hovering things myself. I checked the FLOOR tab and the BLUEPRINTS tab, at desktop width and at phone width. Here is everything, honestly.

## 1. Ten seconds in — what do I think this is?

The big heading says: **"THE ATOMIZE AI PLANT REFINES RAW TEXT INTO INTELLIGENT NEWS."**

Under it: "This is a demo of the part of our news tool that checks facts before they get used, built so you can see exactly what it keeps and what it throws away, and why."

And in small orange caps: "ATOMIZE AI, PIPELINE UNIT 01, A WORKING SCALE MODEL."

My first reaction: it's calling itself a "plant" and a "factory" — like a real physical factory, with hoppers and chutes and gates. I think it's trying to use a factory metaphor to explain something about how AI news gets checked for accuracy. But I genuinely don't know if I'm looking at a real tool, a toy version of a real tool, or a diagram. The words "demo," "working scale model," and "toy" (used later) are all used, and they don't all mean the same thing to me — is this pretend or does it actually do something?

## 2. What does this thing do, in my own words?

Best guess: This is a control panel for a system that reads AI news articles from the internet, decides which facts in them are trustworthy enough to keep, throws out the rest, and stores the good facts somewhere so they can be looked up later (maybe for a podcast or a newsletter, since I saw "daily podcast" mentioned).

I cannot say for certain beyond that. I don't understand HOW it decides what's trustworthy, what "the graph" is, or what happens to the facts after they're stored — the words used to describe those parts are ones I don't know (see below). If you asked me to explain this to a friend, I'd say "it's a filter that only keeps quotes it can find word-for-word in the original article" — that part I actually understood, because of one tooltip. Everything past that, I'm guessing.

## 3. Every word or phrase I did not understand

I'm listing all of these even though some of them "sound like everyday words" — in this context I could not tell what they actually meant:

- "pipeline" (used in "PIPELINE UNIT 01")
- "verbatim quote" (had a tooltip — see #4)
- "grounding gate" / "quote-grounding gate" (had tooltips — see #4)
- "hoppers" (I only understand this as a factory grain funnel; not sure what it means for news)
- "quality gate"
- "reason code" ("every rejection carries the system's real reason code")
- "CONTENT_QUALITY_FLOOR" and all the other ALL_CAPS_WITH_UNDERSCORES labels next to each control
- "ENFORCE_CONTENT_QUALITY_GATE"
- "downstream AI spend" (money? which AI? spending on what?)
- "intake rate"
- "ACQUIRE / TRANSFORM / STORE / RETRIEVE / SURFACE" (a five-step diagram with no plain explanation of what happens at each step)
- "GRAPH VAT" and "the graph" in general — never explained what a graph is here
- "edges" and "entities" ("Entities are rows, edges are an adjacency list keyed by strength")
- "adjacency list"
- "gpgvector" / "pgvector" ("Postgres + pgvector")
- "vector leg" and "keyword leg" ("A vector leg and a keyword leg get fused by a weighted sum")
- "weighted sum," "fused"
- "hybrid search"
- "Reciprocal Rank Fusion" and "k=60"
- "quality guard that can reformulate one weak query"
- "BUILT NOT WIRED" (a badge — is it built or not?)
- "SIM ONLY"
- "spaCy direction check" — I don't know what spaCy is
- "RAGAS run," "gold set," "curated gold set"
- "HNSW" and "IVFFlat" ("Roll back HNSW to IVFFlat")
- "P95 latency," "recall drops below 90%"
- "prisma/migrations/20251013000653_upgrade_to_hnsw_index/rollback.sql" — this is a raw file path shown on the page, I have no idea what to do with this
- "Chunk sizing, 800 target tokens, 100 overlap, 1000 hard max"
- "tokens" (used several times, never explained)
- "openai/gpt-oss-20b" — looks like a code name for something, maybe an AI model?
- "KG block" ("entity extraction runs per KG block")
- "closed vocabulary of 26 types"
- "MEASURED / REASONED / INFERRED / DEFAULT / NO RECORD" (badge legend on the BLUEPRINTS page — explained in a sentence, but a lot to hold in my head)
- "Intent Cascade routing"
- "Class routing," "Class 4.2b" (seen faintly on the diagram)
- "44 of 64 queries retrieve differently, 70.3%" — differently from what?
- "Vercel cron routes," "UTC," "the coldstore," "Railway workers," "queue"
- "content integrity gate," "structural or quality checks"
- "entity extraction," "relationship extraction," "typed, directional links"
- "strength floor"
- "citation check"
- "reject chute"
- "console.ai / news," "atomize V3 feed," "admin inbox" (shown as little boxes, not explained)

That's close to 50 separate terms or phrases I did not understand, on one page.

## 4. Did anything explain a hard word to me? Did it help?

Yes — some words have a dotted underline. I tried hovering two of them: **"verbatim quote"** and **"grounding gate."**

**"verbatim quote" tooltip** said (paraphrasing closely): Quote grounding requires the model to produce the exact sentence a fact came from, or the fact is thrown out. This trades "recall" for "trust" — a real connection stated across two sentences gets lost. Hallucinations fell from 17% to 2.5% under this rule, while a new "ungrounded" category of errors rose to 13%.

**"grounding gate" tooltip** said something very similar but not identical: it drops any fact whose supporting quote can't be found in the source text, checked either exactly or with whitespace normalized.

Verdict: This one partly helped — I now understand the BASIC idea (it only keeps quotes it can find word-for-word). But:
- Two different underlined phrases gave me two overlapping-but-different explanations of what looks like the same thing. That's confusing on its own — are "verbatim quote" and "grounding gate" the same thing or different things?
- The tooltip itself uses more words I don't know: "recall," "trust" (used in a technical sense I don't recognize), "hallucinations," "ungrounded." So the explanation created new questions instead of fully answering the first one.
- I did not try clicking (vs hovering) — clicking those same phrases failed for me technically (the tool couldn't click them, only hover worked), which itself suggests these aren't reliably tappable on a touchscreen.

## 5. Where did I feel stupid, lost, or like the page wasn't written for me?

Almost everywhere past the first two paragraphs. Specifically:

- The moment I hit the "PLANT CONTROLS" panel with sliders labeled "CONTENT_QUALITY_FLOOR" — that's clearly a programmer's internal setting name shown directly to me with no translation.
- The "WHAT-IF LEVERS" panel, which is full of settings like "Grounding strictness," "Edge strength floor," "Search Orchestrator V2 (real RRF fusion)," "spaCy direction check," "Roll back HNSW to IVFFlat" — I don't know what any of these DO to the news I'd actually read, only that turning them on/off does something to numbers I also don't understand (ms, P95, recall).
- The bottom of the FLOOR page ("EVERY PART OF THIS TOY HAS A REAL COUNTERPART IN PRODUCTION") calls the whole thing "this toy" — after being told it's "a working scale model." I don't know anymore if I'm playing with a toy, a demo, or something real that affects a real product.
- The BLUEPRINTS tab is worse — it opens with a legend of six badge types (MEASURED, REASONED, INFERRED, DEFAULT, BUILT NOT WIRED, NO RECORD) I have to memorize before reading anything else, then immediately shows "GATE 02 · Quote-Grounding Gate" with text like "Entity extraction runs per KG block on openai/gpt-oss-20b." I felt like I'd wandered into an engineering document that was never meant for a visitor.
- The little box under the dial labeled "console.ai /news," "daily podcast," "atomize V3 feed," "admin inbox" — I don't know what any of those four things are or how they relate to what I just did above.

## 6. Did I press something and not understand what changed?

Yes, three times:

1. **MODE toggle (REAL SETTINGS / WHAT-IF).** I clicked "WHAT-IF." It turned orange like it was now selected. But the panel right below it still said "Real settings mode: every control below is locked" and showed a button that says "SWITCH TO WHAT-IF" — as if I hadn't switched anything. I expected clicking WHAT-IF once to unlock the sliders below it. It looked like it worked (color changed) but the text said the opposite of what the button showed. I clicked "SWITCH TO WHAT-IF" too, and literally nothing on screen changed. I don't know if I did it wrong or if it's just broken.
2. **"FEED ONE ARTICLE" button.** The page told me "The graph needs at least 5 facts. Feed some articles first, 3 of 5 so far." I clicked "FEED ONE ARTICLE" twice more, expecting the count to go up (4 of 5, then 5 of 5). It stayed at "3 of 5" both times. I expected a number to change and it didn't.
3. **"Gate Power" switch.** This one DID visibly change (ON → OFF, box outline turned orange) — but I scrolled back up to the diagram/counters above and none of the numbers there changed either. So I can't tell if turning it off actually did anything to "the machine," even though the switch itself responded.

## 7. Anything broken, overlapping, cut off, or unreadable?

- **At mobile width (390px):** The two side-by-side panels ("PLANT CONTROLS" and "WHAT-IF LEVERS") do NOT stack into one column — they stay side-by-side and get squeezed narrow. The right-hand "WHAT-IF LEVERS" column becomes noticeably cramped compared to how it reads on desktop. Nothing is technically cut off, but it's clearly not been redesigned for a phone screen — it's a shrunk desktop layout.
- **Raw code artifacts left on screen at any width**, not a rendering bug exactly, but they read as broken to me: a full file path (prisma/migrations/20251013000653_upgrade_to_hnsw_index/rollback.sql) and a model name (openai/gpt-oss-20b) are printed directly on the page like normal sentences. That looks like something a developer forgot to clean up before showing it to a visitor.
- **The server itself timed out on my very first attempt to open the page** ("This site can't be reached... ERR_TIMED_OUT"). I had to try again before it loaded — I'm noting it here even though it's not the page's design, in case it happens to other reviewers too.

## 8. The one change that would help me most

**Give me a one-sentence, plain-English translation next to every single control and badge, written for someone who has never coded — not a tooltip I have to hunt for and hover, and not a second wall of jargon when I do.** Right now almost every label on this page (CONTENT_QUALITY_FLOOR, ENFORCE_CONTENT_QUALITY_GATE, RRF fusion, HNSW/IVFFlat, spaCy, P95, tokens, KG block, adjacency list, gold set...) is either an internal code name or a term from a field I've never studied, and the two tooltips I did find just introduced more jargon on top of jargon. If I can't tell what a control DOES to the news I'd read, in words I already know, I can't use this page at all — I can only click things and watch for a reaction I don't understand.
