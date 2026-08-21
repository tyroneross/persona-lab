# P3 — Peer review: "The Fact Refinery" (Atomize AI eval snapshot)

**Reviewer:** P3, retrieval + knowledge-graph researcher
**Artifact:** `http://127.0.0.1:8777/eval-snapshot.html`, frozen snapshot, 316,383 bytes
**Method:** IBR (screenshot / session / scan) at desktop 1920, 1440 and mobile 390; plus a byte-identical
local mirror of the served file so I could read the shipped `window.M`, `window.G`, `DECK_*` and the
provenance-assignment function directly rather than paraphrasing what the page rendered.
**Reproduction note:** the host server on :8777 became unresponsive mid-review (single-threaded
`python3 http.server`, 4 wedged sockets). I mirrored the exact bytes to :8813 with a threading server and
worked there. Everything below is from those bytes.

**Verdict: REJECT AS AN EVALUATION, ACCEPT AS AN ARCHITECTURE INVENTORY.**
This is an unusually honest map of a codebase and an unusually dishonest artifact to call an evaluation.
It documents parameters. It does not evaluate a system. There is not one retrieval quality number anywhere
on the page — no recall@k, no nDCG, no MRR, no held-out set, no corpus size, not even a row count. The
page knows this about itself and says so in several places, which is to its credit; but the framing
("MEASURED", "the strongest evidence on this page", "the best evidence on the page") does work the
evidence cannot support. Worse, 85% of the provenance badges — the page's central credibility device —
are not judgements at all. They are computed from whether a JSON field is empty.

---

## 1. Is this peer-reviewable?

Partly. The page is auditable as a **claims-about-source-code** document and unauditable as a
**claims-about-system-behaviour** document. The distinction runs cleanly down the middle of the artifact.

### Checkable without access to the repo — internal consistency, arithmetic, definitional coherence

These I checked, and several fail (§2, §3, §4):

| Claim class | Checkable how |
|---|---|
| Index inventory internally consistent with the storage cards | Cross-read the 13-row table against `t-chunks` / `t-vec`. **Fails** on the two-lineage question. |
| Countable claims ("16 Vercel cron routes", "6 Railway workers") | Count the shipped job list. **Passes** — 16 and 6 exactly. |
| Countable claims ("three vector indexes", "six live read paths") | Count. **Both fail** (5 and 11). |
| `0.85` distance → `0.15` minSimilarity | 1 − 0.85 = 0.15. **Passes.** |
| "adaptively tightens to 0.10, 0.08, 0.05, 0.03" | Monotone direction check. **Fails** — those are looser, not tighter. |
| Fusion weights sum to a constant | `0.5 + 0.3(1−q)` + `0.5q` = `0.8 + 0.2q`. **Not normalised**; author never says so. |
| RRF formula `1/(k + rank + 1)`, k=60 | Standard-form check. **Passes** as a formula; **fails** as a design (§2.6). |
| Badge assignment matches badge definitions | Read `provenanceFor()`. **Fails systematically** (§3). |
| Glossary term ↔ definition correctness | Read `window.G` + the linker. **Mostly passes**, with three defects (§6). |
| Hallucination 17% (n=30) → 2.5% (n=120) | Binomial CI check. **Marginal at best** (§2.8). |

### Not checkable at all — every claim about what production does

- Which of the two HNSW indexes on `article_embeddings.embedding` the planner actually uses. The page
  names the resolving query (`pg_indexes`) and does not run it.
- `ENFORCE_CONTENT_QUALITY_GATE` in production. The page reads `.env.example` and — commendably — says
  outright that this is not a claim about production.
- `ENABLE_ENTITY_CONTEXT_PACK` in production, so which graph read path serves by default is unknown.
- Which of the two summarisers production calls.
- Whether the `spa` source rows, the `trending_themes_mv` view, or the `story_clusters` IVFFlat index
  still exist.
- Every latency, throughput, cost and quality number, because none exist except one commit's 92ms/2146ms
  pair and one intent-routing differential.

**Not one number on this page was produced by running the system.** The two MEASURED items are (a) a
pair of manual hallucination audits at n=30 and n=120, and (b) one commit's differential over 64 queries.
Everything else is a constant read out of a file. A reviewer cannot verify a pipeline works by reading
its constants; they can only verify the constants were transcribed. That is what this page supports.

---

## 2. The retrieval and index claims, attacked

### 2.1 The chunk index is called the primary RAG path and no retrieval component reads it

This is the single largest structural hole and it is verifiable with a text search.

Index inventory, row 1, verbatim:

> `idx_embedding_chunks_hnsw` · `article_embedding_chunks` · HNSW · `m=16, ef_construction=64, cosine` ·
> **"chunk retrieval — the primary RAG path"**

Storage card `t-chunks`, verbatim:

> "Embedding Chunks stores one vector per chunk and **is the primary source of retrieval candidates.**"

Now the Retrieve stage. It carries 13 components. I searched every field of all 13 in both the model
object and the authored deck:

```
occurrences of the string "chunk" across all 13 retrieval components = 0
occurrences of "article_embedding_chunks"                            = 0
occurrences of "similarity_search_article_chunks"                    = 0
occurrences of "article_embeddings"                                  = 1
```

The one hit is Hybrid Search, the live default, verbatim:

> "The query is embedded with text-embedding-3-small, then matched by pgvector cosine distance against
> **`article_embeddings`** over an HNSW index."

And `t-vec` describes `article_embeddings` as, verbatim, "one pooled vector per article, used for
clustering and **as the legacy retrieval leg**."

So the page asserts, simultaneously: chunks are the primary retrieval path; article vectors are the
legacy leg; and the only live vector retrieval component queries article vectors. **No component
anywhere on the page calls the chunk retrieval function.** Either "primary RAG path" is aspirational
labelling for an index nothing queries, or there is a retrieval path the 48-card inventory omits. The
page gives the reader no way to tell, and does not list this in its own nine-item conflict register —
which makes it the most important thing the page is hiding.

**Not enough to evaluate. This is disqualifying on its own for a retrieval claim.**

### 2.2 `ef_search=100` is arithmetically incompatible with the seed the chunk function requests

The two facts, both from the page, both verbatim:

> `t-vec`: "A Supabase-side migration sets `hnsw.ef_search=100` at the database level. It is the only
> ef_search value found anywhere in the repo."

> `t-chunks`: "The retrieval function sets `enable_seqscan=off` and pulls a bounded seed of
> `GREATEST(match_count, LEAST(GREATEST(match_count x 64, 512), 8192))` rows ordered by cosine distance."

`ef_search` is the query-time candidate-list width for an HNSW scan. In pgvector, a single HNSW index
scan returns **at most `ef_search` rows** before the index is exhausted; the floor of that seed formula
is 512 and its ceiling is 8192. With `ef_search=100` and `enable_seqscan=off`, the planner cannot
satisfy a request for 512–8192 distance-ordered rows from that index. Three possibilities, and the page
distinguishes none of them:

1. `hnsw.iterative_scan` is enabled (pgvector ≥ 0.8), in which case the page has omitted the parameter
   that makes its own formula work, and omitted `hnsw.max_scan_tuples` with it;
2. the function sets `ef_search` per-transaction and the "only value in the repo" claim is wrong;
3. chunk retrieval silently returns ~100 candidates and the `8192` in that formula is decorative.

Under (3), which is what the page as written implies, the seed formula and the "re-score the top two
chunks per article" step are both operating on a candidate pool an order of magnitude smaller than
advertised, and every downstream `topK` (25/40/60) is drawing from it.

Compounding it: `ef_search=100` was set by a **Supabase migration on the `article_embeddings` lineage**
and is described as database-wide. So a value chosen (if it was chosen) for an `m=24` index is silently
governing an `m=16` index on a different table with a different vector distribution. Nobody measured
either. **Not enough to evaluate.**

### 2.3 The two competing HNSW lineages make every article-vector claim unattributable

Inventory rows 2 and 4, verbatim:

> `article_embeddings_embedding_idx` · `article_embeddings` · HNSW · `m=24, ef_construction=100, cosine` ·
> "article-level similarity; raised above defaults for accuracy"

> `article_embeddings_hnsw_idx` · `article_embeddings` · HNSW · `defaults + hnsw.ef_search=100 set
> database-wide` · **"same column, Supabase lineage — may duplicate the above"**

Maintenance log item 01, verbatim: *"Two migration systems both think they own the same HNSW index …
How to settle it: `Query pg_indexes in production.`"*

The page names the one-line query that resolves this and does not run it. The consequence is not
cosmetic:

- The FLOOR view states flatly, verbatim: *"Article vectors use m=24 and ef_construction=100."* By the
  page's own conflict register that may be false — the serving index may be the `m=16` default one.
  **That sentence is an overclaim the page elsewhere contradicts.**
- If both indexes exist, `article_embeddings` carries three HNSW indexes across two 1536-d columns plus a
  dual-write trigger. The page never mentions the write amplification, the index memory, or the build
  cost of that.
- Any recall or latency statement about article-level search is unattributable to a specific graph.

**Not enough to evaluate.** One `psql` command closes it.

### 2.4 Chunk retrieval: the aggregation rule is missing

> "It then re-scores the top two chunks per article."

Re-scores how? Max-of-two, mean-of-two, sum, or a weighted blend? Chunk→article rollup is *the* design
decision in chunked retrieval — max favours a single strong passage, mean favours diffuse relevance, sum
favours long documents — and it changes the ranking wholesale. The page gives the parameter (`2`) and
withholds the function. `match_count` also has no stated default, so the seed formula cannot be
evaluated numerically at all. **Not enough to evaluate.**

### 2.5 Hybrid search: the direction of the threshold is stated backwards, and the fusion rests on an undefined scalar

Verbatim, from the rendered Hybrid Search card (I captured this on screen, not from source):

> "The distance threshold is 0.85, which gives a minSimilarity of 0.15."
> "That threshold **adaptively tightens** to 0.10, 0.08, 0.05, or 0.03 depending on the top-score band."

0.15 → 0.03 is a **loosening** of a minimum-similarity floor by 5×, described as tightening. Either the
word is wrong or the numbers are, and the page repeats the error in two glossary entries (`recall`:
"adaptively tightens its similarity threshold, trading some recall for predictable latency";
`cosine_distance`: "then tightens it further for weak result sets"), so a reader has no cross-check. Note
also that the stated trade — *tightening* to buy "predictable latency" — is not what a similarity floor
buys you; a floor changes result-set size, not ANN work. The stated rationale does not follow from the
stated mechanism either way.

Then the fusion, verbatim:

> "Fusion is a weighted sum, not RRF: `keywordWeight` equals 0.5 plus 0.3 times (1 minus `vectorQuality`),
> and `vectorWeight` equals 0.5 times `vectorQuality`."

Two objections.

**(a) The weights are not normalised.** Total weight is `0.8 + 0.2·vectorQuality`, so it ranges 0.8→1.0.
Fused scores are therefore not comparable across queries, and the fixed additive boosts (`+0.15` entity,
`+0.20` domain) carry a query-dependent *relative* magnitude — up to 25% more influence on a
low-vector-quality query than a high one. The "0.85 floor rescue" is stated with no mechanism at all.

**(b) `vectorQuality` is never defined anywhere on the page.** Not in the card, not in the glossary
(78 entries, no `vectorQuality`), not in the index inventory. It is the free variable that determines
the entire fusion, and it is the one term the page declines to specify. **This is where the author is
hiding something.** Every other number on this page is sourced to a file and a line; this one is not
sourced at all.

**Not enough to evaluate.**

### 2.6 Reranking: the router that sizes it is switched off, and its "breaker" contradicts the page

Verbatim:

> "Simple and temporal queries use topK 25 on gpt-oss-20b. Complex and conceptual queries use topK 60 on
> gpt-oss-120b. The default is topK 40 on the fast model."

The reranker routes on **query type**. The component that classifies query type is the Intent Cascade —
which the page badges BUILT NOT WIRED and whose own card says both `ENABLE_INTENT_CASCADE_SHADOW` and
`ENABLE_CASCADE_ROUTING` are off. So either (i) the "simple / temporal / complex / conceptual" branches
are dead and every query takes the topK-40 default, making the whole table decorative, or (ii) a second,
unnamed classifier exists that the 48-card inventory omits. The page does not say which. A reviewer
cannot cost or characterise the rerank stage without knowing.

Second: the card says, verbatim, *"A breaker opens for 10 minutes on repeated JSON-validation failures."*
The Cache & Degradation card says, verbatim, *"Nothing in the read path implements true open or half-open
breaker states despite the naming; every breaker here is try-catch-with-fallback or a failure-count
degrade."* And maintenance-log item 08 says the same. **These cannot both be true.** One of them is
wrong and the page ships both.

Third: no rerank quality number exists. Not one. The rerank is the last thing that touches ranking before
a user sees it and its effect size is unmeasured.

### 2.7 Orchestrator V2 / RRF: k=60 over depth-20 lists is barely a fusion

Verbatim: *"real reciprocal rank fusion, with k=60, a per-leg limit of 20, and a score equal to the sum
of 1 divided by (k plus rank plus 1)."*

The formula is fine. The parameterisation is not. With `k=60` and only 20 items per leg, RRF scores span
`1/61` to `1/81` — a 1.33× spread across the entire list. Rank 1 and rank 20 are nearly indistinguishable.
At that ratio RRF degenerates into a membership vote: an item's score is dominated by *how many legs
returned it*, not *where*. If the intent was rank-sensitive fusion, `k` should be small relative to list
depth (Cormack's k=60 was calibrated against TREC runs of depth 1000, not 20). Nobody measured it,
because — verbatim — *"a live RAGAS run never happened, since it needs a database, Groq and a curated
gold set."*

The one measured retrieval number on the whole page is this:

> Speed: baseline **92ms** · cold, V2 **2146ms** · warm, cached **~0ms**. Source: commit `14ee1f714`.

No percentile. No `n`. No hardware. No query set. No statement of the baseline's cache state. "92ms"
without a percentile is not a latency measurement, and comparing a cold uncached V2 against an
unspecified baseline is not a comparison. The page then labels this axis "Speed" and the adjacent axis
"Quality: This axis was never measured" — correctly. It should have applied the same rigour one column
to the left.

### 2.8 The MEASURED grounding number is weaker than the badge implies

Verbatim: *"A first audit found a 17% hallucination rate at n=30. A looser policy shipped … Re-measuring
at n=120 cut hallucinations to 2.5%. A new ungrounded class rose from 0% to 13% at the same time …
[quote grounding] shipped … Its own follow-up note states there were zero rows to re-measure after
deploy. The post-fix rate is not yet re-verified."*

Wilson 95% intervals: 17% at n=30 is roughly [7%, 35%]; 2.5% at n=120 is roughly [0.9%, 7.1%]. The
intervals do not overlap, so the drop is probably real — but the page shows no interval, and the
comparison is confounded three ways at once: different policy, different `n`, different sample, and no
held-out set. Nothing is said about **who judged** a hallucination, against what rubric, or with what
inter-rater agreement. And the fix that this evidence is used to justify — quote grounding — has, by the
page's own admission, **zero post-deploy measurements**. So the strongest evidence on the page is a
before/after on a moving target where the "after" was never taken.

Related, and unaddressed: quote grounding is a **precision-for-recall trade**, and the page's own
glossary says so ("a real relationship stated across two sentences is lost"). The 13% ungrounded class is
reported as a problem to close. Nobody measured how many *true* facts the gate now discards. A gate that
takes hallucinations to 0% by keeping nothing is not an improvement, and the page has no number that
would distinguish that case.

---

## 3. Provenance badge audit — the central defect

The page defines its badges, verbatim:

> MEASURED — a number was actually recorded · REASONED — a written rationale exists in the repository ·
> INFERRED — we read the reason from the code, nobody stated it · DEFAULT — a library or bare constant
> nobody tuned · BUILT NOT WIRED — built and never switched on · NO RECORD — no rationale exists in the
> repository.

Then it assigns them like this (shipped code, unedited):

```js
function provenanceFor(node){
  if(PROVENANCE[node.id]) return PROVENANCE[node.id];
  if(node.status === "dormant")  return { badge:"BUILT NOT WIRED", ... };
  if(node.dec && node.dec.length) return { badge:"INFERRED", ... };
  return { badge:"NO RECORD", ... };
}
```

`PROVENANCE` has **7 hand-authored entries**. There are **48 component cards**. So **41 of 48 badges
(85%) are derived from whether an author left a `dec` array empty.** The resulting distribution:

| Badge | Count | How assigned |
|---|---|---|
| INFERRED | 33 | automatic — `dec` array non-empty |
| NO RECORD | 7 | automatic — `dec` array empty |
| DEFAULT | 4 | hand-authored |
| BUILT NOT WIRED | 3 | 2 hand-authored, 1 automatic (`status === "dormant"`) |
| REASONED | 1 | hand-authored |
| **MEASURED** | **0** | — |

**Zero of the 48 component cards carry MEASURED.** The badge is defined in the legend at the top of the
view and then never used below it. Both MEASURED badges on the site live on the FLOOR view.

### Badges that are individually wrong

**Overclaiming an absence — NO RECORD is a claim about the repository that nobody checked.**
"No rationale exists in the repository" is a strong negative assertion. It is emitted whenever a `dec`
array is empty. Named individually:

1. **`s-podgen` (On-Demand Podcast) — NO RECORD.** Its own card says, verbatim, *"The rate limiter is
   in-process rather than Redis-backed, which is marked TODO in the source."* A TODO in the source *is*
   a written record of the rationale. The badge is contradicted by the card it sits on.
2. **`t-ops` (Ops & Queues) — NO RECORD.** The card states three deliberate design positions
   (database-backed breaker not Redis; `Float[]` "because nothing searches it"; a polling queue kept
   separate from the BullMQ broker). "Because nothing searches it" is a stated reason.
3. **`t-theme` (Trends & Themes) — NO RECORD.** The card carries a substantive structural finding
   (`centroid_vector` is `Float[]`, so no ANN index is possible) and an open question about
   `trending_themes_mv`.
4. **`summ` (Summarisation) — NO RECORD.** The page's own maintenance log, item 03, documents the
   two-summariser ambiguity and names the file that resolves it. There is a record; it is on the same page.
5. **`r-theme` (Custom Themes) — NO RECORD.** Its unsettled note is an *analysis* of a vestigial
   `max-age=900` header.
6. **`s-feed` (V3 Article Feed) — NO RECORD**, and 7. **`signals` — NO RECORD**, both for the same reason:
   nobody wrote a `dec` line.

None of these seven were checked for the absence of a rationale. The badge asserts a negative derived
from an authoring gap.

**`s-digest` (Persona Digest) — BUILT NOT WIRED. Factually wrong.** The badge is defined as "built and
never switched on." It was auto-assigned because `status === "dormant"`. The card's own text says the
opposite, verbatim: *"Release rows with social signals and persona implications. **Still deployed, no
longer consumed** … after /news moved from a news-list layout to the market map."* It was wired, then
unwired. "Never switched on" is false.

**`r-intent` (Intent Cascade) — BUILT NOT WIRED, and the card contradicts itself and the other view.**
Three inconsistencies in one component:
- Headline, verbatim: *"A three-tier query classifier **already runs on every search**, but today only
  whispers."* Mechanism, verbatim: *"It **runs** non-blocking inside a 250 millisecond budget and today
  only produces clarification chips."* Tradeoff, verbatim: *"`ENABLE_INTENT_CASCADE_SHADOW` and
  `ENABLE_CASCADE_ROUTING` are both off, so it observes without altering retrieval."* If the shadow flag
  is off, it does not run. "Already runs on every search" and "shadow is off" cannot both be true.
- "Built and never switched on" contradicts "already runs on every search" within the same card.
- **The same component is badged MEASURED on the FLOOR view and BUILT NOT WIRED on BLUEPRINTS.** Two
  badges, one component, two views, no reconciliation.

**Cross-view badge conflict on chunk sizing.** FLOOR badges chunk sizing **REASONED**, citing
`docs/plans/2026-08-06-chunked-embeddings-ingestion-capacity.md`. BLUEPRINTS badges the `embed` component
**INFERRED**, whose note reads *"This rationale is read from the structure of the code, not quoted from a
stated decision."* There is a plan document. INFERRED is wrong.

**Underclaiming — INFERRED applied where a written record is quoted on the card itself.** INFERRED means
"nobody stated it." These five cards quote someone stating it:

1. **`t-mv` (Materialised Views) — INFERRED.** Card, verbatim: *"**The route comment** marks 30 minutes as
   provisional and names the metric that would justify lengthening it."* A quoted route comment is a
   written rationale. → REASONED.
2. **`t-user` (Users & Saved) — INFERRED.** Card, verbatim: *"Both … are **documented workarounds** for
   Prisma 7's driver-adapter pattern disabling prisma migrate."* → REASONED.
3. **`r-trend` (Clusters & Trends) — INFERRED.** Card, verbatim: *"The legacy Louvain … path is explicitly
   excluded from the request path, **per an in-repo ADR**."* An ADR is the canonical form of a written
   rationale. → REASONED.
4. **`t-content` (Article Content) — INFERRED.** Card cites a dated production incident (2026-06-30) and
   the schema change made in response. → REASONED at minimum.
5. **`s-contact` (Recommendation Form) — INFERRED.** Card records an observed failure — *"roughly three
   months of silent 503s"* — which is an observation, not an inference.

And **`src-reg` — INFERRED**, whose `dec` cites *"a 2026-06-13 audit found zero genuinely JS-only
sources."* An audit produced a count. That is closer to MEASURED than INFERRED.

The one honestly-labelled INFERRED on the page is **`r-explore`**, whose rationale reads *"most plausibly
for query-plan predictability"* — hedged, and correctly badged. It is the exception that shows the rest
were never individually judged.

**Net effect:** the badge system reads as a per-component evidentiary judgement and is, for 41 of 48
cards, a field-presence check. That is a stronger epistemic claim than the mechanism can support, and it
is the thing on this page most likely to mislead a reader who trusts it.

*(Credit where due: the hand-authored `gate` note is exemplary — "Only the sample environment was checked
here, so this is not a claim about what production runs." That is exactly the right register. The problem
is that only 7 cards got that treatment.)*

---

## 4. Where synthetic illustration is confused with real measurement

**4.1 "Graph trust: 96%" is a fabricated metric presented as a live gauge, with no synthetic tag.**
The gauge row carries per-gauge provenance sub-labels. Three of them say "synthetic, no external
baseline" (`articles fed`, `rejects / min`, `queries served`). **`graph trust` does not.** Its sub-label
reads only *"starts at 96%, floor 15%"* — a range, phrased like a calibration, not a disclaimer. Nothing
in the system produces a "graph trust" figure; there is no such field in any of the 48 components, the
index inventory, or the ledger. It is invented for the toy, it is driven by the two sliders whose badges
are MEASURED and DEFAULT, and it renders as a percentage adjacent to 17% / 2.5% / 13% hallucination
rates that *are* real. That adjacency is the confusion.

**4.2 `12.0 intake / min` is untagged too.** Sub-label, verbatim: *"max 12.0 with all 5 open."* A rate,
to one decimal, with a unit — and unlike its three neighbours, no "synthetic" marker. Inconsistent
tagging inside a single row of eight gauges.

**4.3 The closing claim is falsified by the page's own conflict register.** Section 04, verbatim:

> "Every parameter on this page, the 0.5 quality floor, the 0.5 edge strength floor, the 16 cron routes
> and 6 Railway workers, **is read from the Atomize codebase.** The particles, the timings and the counts
> are synthetic illustration."

"Read from the codebase" is doing sleight of hand. `ENFORCE_CONTENT_QUALITY_GATE=false` was read from
`.env.example`, which the page elsewhere admits is *not* production. `m=24 / ef_construction=100` was read
from a migration that may be shadowed by a second index. The blueprint footer's *"Every parameter on these
pages was read from the codebase in August 2026"* has the same problem. Reading a constant out of a file
is not the same as knowing the system runs it, and the closing line elides exactly that distinction after
the body text spent 48 cards being careful about it.

**4.4 "The team measured it carefully on real production traffic" — Section 02 headline claim.**
The panel then says, verbatim: *"The golden corpus holds 64 hand-authored cases, not real traffic."*
What was measured on production traffic was the **differential** (do results change), n=64. What was
measured at 39.1% → 59.4% was **accuracy on hand-authored cases**. The intro sentence merges the two and
attributes the accuracy gain to production traffic. It did not happen there.

The same panel reports **"28 better / 4 worse / 13 neutral"** with no rater named, no rubric, no blinding,
and no agreement statistic. 45 judged, 19 unjudged out of 64, unexplained. This is the page's flagship
evidence and its methodology section is one word: "judged."

**4.5 Correctly handled, and worth naming as the standard the rest should meet.** The Gate Power note:
*"The rejection rate this toggle produces below is **invented by the toy**, not measured from the real
system."* The reject-chute header: *"real reason codes, synthetic counts."* The canvas stamp: *"SYNTHETIC
RUN, not telemetry."* The V2 quality axis: *"This axis was never measured."* When this page is honest it
is better than most engineering documentation I review. It is simply not honest uniformly.

---

## 5. What a reviewer would demand before believing the system works

In priority order. Items 1–3 are cheap enough that their absence is itself evidence.

1. **Corpus size. Any count at all.** There is not one row count on this page — not articles, not chunks,
   not entities, not edges. `m=16` versus `m=24` is meaningless without N; HNSW's recall/latency curve is
   a function of graph size. The page even tells us the index decision was validated on a test database
   holding **4 rows** (`.claude/INDEX_DECISION_SUMMARY.md`) and never says what production holds. This is
   the most conspicuous omission in the document.
2. **`SELECT * FROM pg_indexes WHERE tablename IN ('article_embeddings','article_embedding_chunks')`.**
   The page names this query as the resolution to its own top conflict. One command, and every
   article-vector claim becomes attributable.
3. **ANN recall@k against exact kNN at the deployed `ef_search`.** Brute-force `ORDER BY embedding <=> q
   LIMIT k` with `enable_indexscan=off`, compare to the indexed result, for both indexes, at k ∈ {10, 50}.
   A morning's work. Its absence, on a page whose entire subject is index parameters, is the gap.
4. **A retrieval eval set with graded relevance, and nDCG@10 / recall@50 / MRR for the four
   configurations the page describes**: lexical, hybrid weighted-sum, hybrid + rerank, RRF V2. The page
   admits RAGAS was never run. Without this, "Orchestrator V2 is better" and "reranking helps" are
   both unfalsifiable.
5. **Latency distributions, not point estimates.** p50/p95/p99 per read path under representative
   concurrency. `92ms` is not a measurement.
6. **The hallucination audit protocol.** Sampling frame, annotator identity and count, rubric,
   inter-annotator agreement, confidence intervals — and a **post-deploy re-measurement of quote
   grounding**, which the page says was never taken because there were zero rows.
7. **The precision cost of quote grounding.** How many true relationships does the verbatim-span
   requirement discard? Without this, the 17% → 2.5% number cannot be read as an improvement.
8. **A definition of `vectorQuality`,** and normalised fusion weights or an argument for why unnormalised
   is correct.
9. **The chunk→article aggregation function,** and the default `match_count`.
10. **Dedupe precision/recall for `createGuidHash`.** The page describes a SHA-256 over normalised title +
    link + date bucket and reports no false-merge or false-split rate. The "dupes folded" gauge is
    synthetic.
11. **Embedding-version migration cost.** `EMBEDDING_VERSION v1` is stamped so a model swap is
    "detectable" — with no statement of what re-embedding the corpus would cost or take.

---

## 6. Glossary — tested, and it is the best-written part of the page wired the worst

**Content quality: high.** 78 entries, each with a `what` (plain-language) and a `why` (grounded in this
specific system). The `pgvector`, `cosine_distance`, `pooling`, `adjacency_list`, `quote_grounding` and
`circuit_breaker` entries are all accurate and non-generic — `circuit_breaker` even flags that the
codebase's breakers are misnamed. I checked all the retrieval and index entries against their cards.

**Terms tested live via IBR (hover on FLOOR, desktop 1440):**

| Term | Opens? | Defines the right thing? |
|---|---|---|
| "verbatim quote" → `quote_grounding` | yes | yes |
| "grounding gate" → `grounding_gate` | yes | yes |
| "vector leg" → `vector_search` | yes | yes |
| "reranked" → `reranker` | yes | yes |
| "queue events" → `queue_driven` | yes | yes |
| "dedupe", "SSRF guard", "pgvector", "adjacency list" | yes (band panels) | yes |
| Any term inside a BLUEPRINTS component card | **hover only — not keyboard, not screen reader** | yes |

No anchor points at a missing definition; all 9 hand-placed `data-term` keys exist in `window.G`.

### Defect 1 — 64 of 78 definitions are unreachable in BLUEPRINTS, including `ef_search`

The blueprints auto-linker holds **14** of the 78 terms:

```
pgvector, hnsw, m, ef_construction, tsvector, gin, bullmq, ssrf,
cl100k_base, ivfflat, jsonb, materialized_view, idempotent, circuit_breaker
```

There is **no regex for `ef_search`, `rrf`, `weighted_sum_fusion`, `topk`, `recall`, `ann`,
`cosine_distance`, `reranking`, `chunk`, `pooling`, `embedding`, `vector_1536`, `vector_cosine_ops`,
`text_embedding_3_small`, `multi_hop`, `traversal`, `grounding`** or 47 others. `ef_search` — the
query-time parameter this whole review turns on — has a full, correct, well-written definition that **no
reader can ever open in the blueprints view.**

Consequence I verified by simulating the linker over the shipped deck: all 14 links land in the Acquire,
Transform and Store bands. **Zero glossary links appear in the Retrieve or Surface bands.** The 13
retrieval cards — the densest jargon on the page (`RRF`, `topK`, `minSimilarity`, `vectorQuality`,
`stale-while-revalidate`, `recursive CTE`, `HNSW`) — carry not one definition.

### Defect 2 — each term links exactly once in the whole view; and the two value-pinned regexes point at the wrong number

The linker carries `if(usedTerms[g.term]) return;` — a term is marked once and never again.

| Term | Occurrences in blueprint content | Linked |
|---|---|---|
| HNSW | 19 | 1 |
| GIN | 18 | 1 |
| pgvector | 9 | 1 |
| `m=24` | 6 | **0** |
| `ef_construction=100` | 5 | **0** |
| `ef_search` | 5 | **0** |

I confirmed this on screen: the Hybrid Search card renders "pgvector cosine distance … over an HNSW
index" with no dotted underline on either term, because the Store band consumed them first.

Worse, two regexes are pinned to a literal value:

```js
{term:"m",               re:/\bm=16\b/},
{term:"ef_construction", re:/\bef_construction=64\b/},
```

So the popovers are titled **"m = 16"** and **"ef_construction = 64"** and fire only on the `t-chunks`
card — the DEFAULT, untuned index. The `t-vec` card, carrying `m=24 / ef_construction=100`, the one
parameter choice on this page with a written rationale behind it, gets **no glossary link at all**. The
page's glossary teaches the reader the value the page itself says nobody thought about, and withholds the
value the page says someone did.

### Defect 3 — every blueprint glossary term is keyboard- and screen-reader-inaccessible

`armTerms()` sets `tabindex="0"`, `role="button"` and an `aria-label` carrying the definition. It is
called exactly twice: at its definition, and once at boot as `armTerms(document)`. But band content is
injected **after** boot — `openStage()` does `bandEl.innerHTML = bandHTML[sid]` and never calls
`ctx.armTerms(bandEl)`, even though `armTerms` is passed into the blueprints module for that purpose.
Dead wiring.

Verified two ways: reading the source, and via IBR's accessibility tree with the Store band open — 18
interactive elements reported, none of them a `.gl` span. Hover still works (the listeners are delegated
on `document` and match by class), so a mouse user is fine. A keyboard user cannot reach a single
definition in the blueprints view, and a screen reader announces the bare word with no definition
attached. Note the FLOOR view's nine hand-placed terms *are* armed correctly — so the page proves it
knows how, and then drops it on the 48 cards.

### Defect 4 — a duplicate entry that can never fire, and one misplaced first-use

`window.G` contains **two entries both titled "GIN index"**: `gin` and `gin_index`, with different
bodies. The linker's regex maps to `gin`, so `gin_index` is dead data.

And the single `materialised view` link fires on the `t-theme` card, inside a *"Still unsettled"* note
about a view that *"may never have gone live."* The `t-mv` card — the component actually about
materialised views — has no link. The one place a reader can learn the term is attached to the one
instance of it that might not exist.

---

## 7. Visibly broken, misaligned, cut off, or unreadable — with widths

**7.1 The page ships no `<meta name="viewport">`. Every mobile breakpoint the author wrote is dead code
on a real phone. — 390 px.**

The served document contains **zero `<meta>` tags of any kind**. It begins at `<title>`. Without
`width=device-width`, mobile Safari and Chrome use a ~980 px layout viewport and downscale the whole page.

I proved this with a control. Same bytes, one line added (`<meta name="viewport" content="width=device-width,
initial-scale=1">`), same 390×844 render:

- **As shipped, 390 px:** the 5-column stage schematic renders as 5 columns; the 6-column INDEX INVENTORY
  table renders at full width; the three GATE cards render side by side. Body copy at `0.9375rem`
  downscales to ≈ 6 CSS px; the `11px` mono in the index table and maintenance log renders at ≈ 4.4 px.
  The index inventory and the maintenance log are **illegible**.
- **With the meta tag, 390 px:** the `max-width:480px` rule fires exactly as written — schematic collapses
  to one column, cards stack, type is fully legible.

The author wrote three careful breakpoints (`900px`, `640px`, `480px`) including `grid-template-columns:1fr`,
`min-height:44px` touch targets and `.bp-close{width:100%}`. **None of them can ever execute.** The CSS is
correct; the document never opts in.

**7.2 Provenance badges measure 60 × 21 px on desktop — below the 24 px minimum — and ≈ 8 pt on a phone.**
IBR's touch-target rule flags `#badgeFloor`, `#badgeGate` and siblings at **60 × 21 px** against a 24 × 24
desktop minimum. Combined with 7.1, the effective scale factor on a 390 pt phone is 390/980 ≈ 0.398, so a
21 px badge renders ≈ **8.4 pt tall** against Apple's 44 pt minimum. The page's single most important
interactive affordance — the control that reveals *why a number should be believed* — is the hardest thing
on the page to hit.

**7.3 The WHAT-IF LEVERS column is a near-empty half-screen. — 1920 px.**
In section 01, the left PLANT CONTROLS panel runs the full height of the section (quality floor, gate
power, five source rows, three action buttons). The right WHAT-IF LEVERS panel renders its header, the
Real/What-if toggle, one sentence, and a collapsed `<details>` — then stops, leaving roughly three-quarters
of the column as empty dark space down to the machine canvas. The asymmetry reads as a rendering failure
rather than a design choice, and the collapsed *"Five more settings, with their evidence"* is where four
of the page's six provenance-badged parameters are hiding.

**7.4 The blueprints view can only hold one band open at a time, so find-in-page misses 39 of 48 cards.**
`openStage()` writes into a single shared `bandEl`; `closeStage()` sets `innerHTML = ""`. Opening Retrieve
destroys Store. For a 48-card provenance inventory whose whole purpose is auditing, Cmd-F cannot reach
39 of 48 cards at any given moment, and the reader can never put Store and Retrieve side by side — which
is exactly the comparison §2.1 requires.

**7.5 `?view=blue` is written but the state is otherwise unshareable.** `swap()` calls
`history.replaceState(… '?view=' + next)` and the boot code does honour `?view=blue` on load — that part
works. But nothing encodes which band is open or which card is expanded, so a reviewer cannot link a
colleague to a specific component card. For an artifact whose purpose is review, no deep links.

**7.6 The document carries no `<meta charset>` and no `<html lang>`.** It is entirely dependent on the
server sending `charset=utf-8`. I hit this directly: serving the identical bytes from a host that omits
the charset renders `▾Controls` as `â-¾Controls` and every apostrophe in section 04 as `â€™`. The host at
:8777 does send the header, so the page renders correctly there — but the document is not self-describing,
and it uses `▸ ▾ · — × ≥ £` throughout. Save it to disk, open it over `file://`, or serve it from a
misconfigured host and the typography breaks.

**7.7 Wordmark clips at narrow width. — ≤ 480 px (control render).** "THE FACT REFINERY" renders as
"FACT REFINERY"; the article is dropped. Cosmetic, and only observable once 7.1 is fixed.

**7.8 Idle canvas dead band. — all widths.** At rest the machine's RETRIEVE row renders as an empty
labelled strip with no risers until a query is run. One fifth of the diagram is blank on first paint,
with no affordance pointing at "Run a query."

**7.9 Instrument caveat — do not act on these.** IBR's scan reports 84 "looks interactive but has no
handler" errors and a FAIL verdict. **These are false positives.** The page uses `document`-level event
delegation throughout, which the handler-integrity rule structurally cannot see; I confirmed the tab
buttons, badges and glossary terms all respond. Likewise the 0×0 px measurements on "Real" / "What-if" /
"Controls" are the sticky bar measured while hidden. The scan's touch-target and contrast numbers (14/15
text pairs pass; the failing pair is not named in the summary) are the parts worth keeping.

---

## 8. The single change that would most improve credibility

**Run one recall@k measurement against exact kNN, on the index that actually serves, and put the number
on the page — then let the badge system be honest about how little else is measured.**

Concretely, and it is under an hour:

```sql
-- 1. settle which index exists (the page names this query and never runs it)
SELECT indexname, indexdef FROM pg_indexes
WHERE tablename IN ('article_embeddings','article_embedding_chunks');

-- 2. ground truth
SET enable_indexscan = off; SET enable_seqscan = on;
SELECT id FROM article_embedding_chunks ORDER BY embedding <=> $1 LIMIT 50;

-- 3. what the system actually returns
SET enable_indexscan = on; SET hnsw.ef_search = 100;
SELECT id FROM article_embedding_chunks ORDER BY embedding <=> $1 LIMIT 50;
```

Intersection ÷ 50, over ~200 held-out queries. Report `recall@50` with the corpus row count beside it.

Why this one and not the others:

- It converts the page's central subject — `m`, `ef_construction`, `ef_search`, two competing lineages —
  from transcription into evidence. Right now the page reports six index parameters and cannot say what
  any of them buys.
- It is the cheapest possible falsification of §2.2. If recall@50 is high, `ef_search=100` is fine and my
  objection dissolves. If it is 0.3, the page has found a live production defect and the whole artifact
  becomes valuable rather than merely careful.
- It forces the corpus size onto the page, closing the largest omission (§5.1).
- It would populate **MEASURED at least once** in the blueprints view, where the badge is currently
  defined in the legend and used zero times across 48 cards.

Second-priority, and nearly free: **stop deriving badges from field presence.** Replace
`provenanceFor()`'s three fallback branches with an explicit per-component judgement, or — if 48 hand
judgements is too much work — collapse the auto-assigned cases into a single honest badge reading
**NOT ASSESSED**. A page whose thesis is "here is exactly how well we know each number" cannot compute
41 of its 48 epistemic claims from `if (array.length)`. Right now the badges are the most confident thing
on the page and the least earned, and that inversion is what a reviewer will hold against everything else.

---

## Appendix — countable claims checked

| Claim | Where | Verdict |
|---|---|---|
| "Sixteen Vercel cron routes" | FLOOR §03 | ✅ 16 |
| "Six Railway workers" | FLOOR §03 | ✅ 6 |
| 48 component cards (9+9+9+13+8) | BLUEPRINTS | ✅ 48 |
| 13-row index inventory | BLUEPRINTS §03 | ✅ 13 |
| 9 maintenance-log conflicts | BLUEPRINTS §04 | ✅ 9 |
| "Nine groups, **three vector indexes**" | FLOOR, Store band panel (`stage.sub`) | ❌ inventory lists **5** (4 HNSW + 1 IVFFlat) |
| "**Six live read paths** plus two dormant" | Retrieve stage `sub` | ❌ **11 live** + 2 dormant among 13 components |
| `0.85` distance → `0.15` minSimilarity | Hybrid Search | ✅ |
| "tightens to 0.10, 0.08, 0.05, 0.03" | Hybrid Search + 2 glossary entries | ❌ direction inverted |
| Fusion weights sum to 1 | Hybrid Search | ❌ sum is `0.8 + 0.2·vectorQuality` |
| 28 + 4 + 13 judged of 64 differential queries | FLOOR §02 | ⚠️ 45 of 64; 19 unaccounted, no rater, no rubric |
| 45/64 = 70.3% retrieve differently | FLOOR §02 | ✅ 70.3% |
| MEASURED badges on the 48 component cards | BLUEPRINTS | ❌ **0** |
