---
id: debug-rag-on-milvus.md
title: Debug RAG on Milvus with a 16 Problem Checklist
summary: Use a symptom-first 16 problem map to debug indexing, filtering, retrieval, and grounding failures in Milvus based RAG pipelines.
---

# Debug RAG on Milvus with a 16 Problem Checklist

This page helps debug Milvus based RAG failures when the database is running, queries return results, but retrieval quality is unstable, misleading, or wrong.

Start from the symptom navigator, jump to the matching problem number, then apply the smallest safe fix before changing anything else.

This page focuses on retrieval, indexing, filtering, and grounding behavior. It is not a model benchmark guide.

## Start here by symptom

<a id="symptom-navigator"></a>

If you are not sure which problem number fits your case, start here.

| What you see | Start with |
| --- | --- |
| The correct data exists, but it does not show up in top results | [No.2](#no2), [No.5](#no5), [No.9](#no9), [No.11](#no11) |
| Results look related, but they answer a neighboring question | [No.1](#no1), [No.3](#no3), [No.13](#no13) |
| Retrieval got worse after reindexing or incremental updates | [No.4](#no4), [No.6](#no6), [No.10](#no10) |
| Deleted, stale, or deprecated content still appears | [No.6](#no6), [No.7](#no7), [No.14](#no14) |
| Filters make results sparse, empty, or obviously worse | [No.8](#no8), [No.9](#no9), [No.11](#no11) |
| Top results are repetitive and lack diversity | [No.11](#no11), [No.12](#no12) |
| The final answer blends facts from multiple sources | [No.13](#no13), [No.14](#no14), [No.15](#no15) |
| A change seems helpful once, but nobody can prove the system improved | [No.10](#no10), [No.16](#no16) |

## 16 Problem Map by stage

<a id="quick-index"></a>

Use this quick index if you already know roughly where the pipeline is failing.

### Stage 1. Query and input formation

| No. | Problem | What it usually looks like | Jump |
| --- | --- | --- | --- |
| 1 | Query intent drift | Results are related, but they answer the wrong question | [Go](#no1) |
| 2 | Chunk to retrieval mismatch | The right source exists, but the answer-bearing chunk never surfaces | [Go](#no2) |
| 3 | Embedding model mismatch | Semantically obvious matches are missing | [Go](#no3) |
| 4 | Metric mismatch | Ranking feels noisy or unstable even when data looks correct | [Go](#no4) |

### Stage 2. Ingestion and storage consistency

| No. | Problem | What it usually looks like | Jump |
| --- | --- | --- | --- |
| 5 | Partial ingestion | Only part of the knowledge base is retrievable | [Go](#no5) |
| 6 | Update skew after incremental writes | New facts appear inconsistently or lose to old facts | [Go](#no6) |
| 7 | Delete visibility drift | Deleted or deprecated content still appears | [Go](#no7) |
| 8 | Collection or partition routing mistakes | Search works, but it queries the wrong dataset | [Go](#no8) |

### Stage 3. Retrieval and ranking

| No. | Problem | What it usually looks like | Jump |
| --- | --- | --- | --- |
| 9 | Filter overconstraint | Valid candidates disappear after filters are applied | [Go](#no9) |
| 10 | Index or search parameter mismatch | Recall and latency swing across runs | [Go](#no10) |
| 11 | Candidate starvation | The answer feels under-informed because too few candidates survive | [Go](#no11) |
| 12 | Duplicate and near duplicate collapse | Top results are filled with repeated evidence | [Go](#no12) |

### Stage 4. Grounding and answer assembly

| No. | Problem | What it usually looks like | Jump |
| --- | --- | --- | --- |
| 13 | Context packing disorder | Good evidence is retrieved, but the answer still misses it | [Go](#no13) |
| 14 | Cross document contamination | The answer blends incompatible sources | [Go](#no14) |
| 15 | Citation and provenance loss | The answer cannot reliably show where claims came from | [Go](#no15) |
| 16 | Verification gap | Changes are judged by anecdotes instead of repeatable checks | [Go](#no16) |

## Fast elimination flow

Before tuning multiple layers, use this quick elimination path:

1. Confirm the expected document exists in the intended collection or partition.
2. Confirm the query embedding contract matches the stored embedding contract.
3. Remove filters and compare results against the filtered version.
4. Increase the candidate pool and check whether missing evidence appears.
5. Confirm inserts, updates, and deletes are reflected in what search can actually retrieve.
6. Inspect the final prompt and verify source boundaries are preserved.
7. Re-run the same fixed query set before and after each change.

## Detailed breakdown

## Stage 1. Query and input formation

<a id="no1"></a>

### No.1 Query intent drift

**What you see**  
Retrieved chunks look semantically close, but they answer a neighboring question instead of the actual task.

**What it usually means**  
The retrieval query no longer matches the original user intent because rewriting, expansion, or application side preprocessing changed what is being searched.

**What to inspect in Milvus**  
Inspect the final query text used to generate embeddings, any query rewriting layer, and any tenant, scope, or prefix logic applied before search.

**Smallest safe fix**  
Separate the original user question, the retrieval query, and the answer prompt. Keep the retrieval query tightly aligned to the real intent.

**How to prove it**  
Run the same request once with query rewriting enabled and once without it. Compare the top results side by side.

**Often confused with**  
[No.13](#no13), because bad context packing can also make the final answer look off-topic even when retrieval was correct.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no2"></a>

### No.2 Chunk to retrieval mismatch

**What you see**  
Relevant source material exists, but top results contain fragments that miss the exact fact needed.

**What it usually means**  
Chunk boundaries split the evidence into pieces that are too small, too large, or poorly aligned with how the query retrieves context.

**What to inspect in Milvus**  
Inspect the chunking logic before insertion, including overlap size, heading boundaries, code block handling, and table extraction.

**Smallest safe fix**  
Rechunk documents so each vector stores one coherent retrievable unit. Use overlap only where it improves continuity.

**How to prove it**  
Run a fixed query set and check whether the exact answer-bearing chunk now appears in the top candidates.

**Often confused with**  
[No.11](#no11), because too small a candidate pool can also hide the right chunk.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no3"></a>

### No.3 Embedding model mismatch

**What you see**  
The pipeline returns results, but obvious semantic matches are missing or ranked surprisingly low.

**What it usually means**  
Stored vectors and query vectors were produced by different embedding models, different revisions, or incompatible preprocessing rules.

**What to inspect in Milvus**  
Inspect the exact embedding model name, normalization behavior, truncation policy, and whether historical data was embedded under a different contract.

**Smallest safe fix**  
Use one embedding contract for both indexing and querying. Re-embed data if that contract changed.

**How to prove it**  
Prepare a small gold set of known query to document pairs and compare recall before and after re-embedding.

**Often confused with**  
[No.4](#no4), because metric mismatch can look similar even when the embedding model itself is consistent.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no4"></a>

### No.4 Metric mismatch

**What you see**  
Results feel noisy, unstable, or oddly ordered even when embeddings seem correct.

**What it usually means**  
The chosen similarity metric does not match the embedding model assumptions, or normalization is inconsistent.

**What to inspect in Milvus**  
Inspect the index metric type, the normalization policy, and whether the embedding model expects cosine style comparison or another distance behavior.

**Smallest safe fix**  
Align metric choice and normalization with the embedding model guidance, then rebuild the affected index if needed.

**How to prove it**  
Run the same benchmark queries before and after the metric correction and compare rank stability.

**Often confused with**  
[No.10](#no10), because poor search parameter choices can also create unstable ranking.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

### Stage 1 summary

If the answer starts improving when you restore the original query, re-check query formation before tuning retrieval.  
If obvious semantic matches are still missing, stay in Stage 1 until embedding contract and metric alignment are clean.

## Stage 2. Ingestion and storage consistency

<a id="no5"></a>

### No.5 Partial ingestion

**What you see**  
Only part of the expected knowledge base is retrievable, even though the pipeline completed without a hard failure.

**What it usually means**  
The ingestion job skipped files, failed mid-batch, or inserted only a subset of the intended records.

**What to inspect in Milvus**  
Inspect expected source counts, insert batch counts, collection totals, and whether all intended partitions were populated.

**Smallest safe fix**  
Add a strict completeness check for ingestion and re-run only the missing slice before evaluating retrieval quality.

**How to prove it**  
Compare source record totals against inserted entity totals and confirm the missing gap disappears.

**Often confused with**  
[No.8](#no8), because routing to the wrong collection can also make the store look incomplete.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no6"></a>

### No.6 Update skew after incremental writes

**What you see**  
Recently updated content does not consistently outrank stale content, or new facts appear only sometimes.

**What it usually means**  
Incremental writes updated only part of the data, while old vectors or stale companion records still remain searchable.

**What to inspect in Milvus**  
Inspect update logic, upsert rules, duplicate IDs, and whether older versions are retired consistently.

**Smallest safe fix**  
Define one canonical update path. Overwrite or retire stale records instead of letting old and new versions compete.

**How to prove it**  
Use a query tied to a recent fact change and verify that only the newest version dominates top results.

**Often confused with**  
[No.7](#no7), because delete visibility problems can also make stale content survive.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no7"></a>

### No.7 Delete visibility drift

**What you see**  
Deleted, deprecated, or invalid content still appears in retrieved evidence or final answers.

**What it usually means**  
Deletion state, retention rules, or application side visibility logic is not aligned with what the retriever still searches.

**What to inspect in Milvus**  
Inspect delete flow, tombstone handling, visibility filters, and any application side rule that should suppress retired records.

**Smallest safe fix**  
Make deletion state part of the retrieval contract and exclude deleted content consistently.

**How to prove it**  
Run known queries against removed content and confirm it no longer surfaces.

**Often confused with**  
[No.6](#no6), because incomplete updates can also make old content appear active.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no8"></a>

### No.8 Collection or partition routing mistakes

**What you see**  
Search returns results, but they come from the wrong dataset, wrong tenant, or wrong partition.

**What it usually means**  
Application routing is sending the request to the wrong collection or using inconsistent partition selection rules.

**What to inspect in Milvus**  
Inspect collection name resolution, tenant mapping, partition keys, and any environment based routing logic.

**Smallest safe fix**  
Make routing explicit, testable, and logged for every search request.

**How to prove it**  
Run tenant specific or dataset specific test queries and verify that search only touches the intended target.

**Often confused with**  
[No.9](#no9), because over-strict filters can also make the correct dataset seem invisible.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

### Stage 2 summary

If the store itself is incomplete, stale, or routed incorrectly, do not tune ranking yet.  
Fix storage truth first, then return to retrieval behavior.

## Stage 3. Retrieval and ranking

<a id="no9"></a>

### No.9 Filter overconstraint

**What you see**  
Results are sparse, empty, or clearly worse after metadata filters are applied.

**What it usually means**  
Filters exclude valid candidates through overly strict conditions, wrong field values, or schema mismatches.

**What to inspect in Milvus**  
Inspect filter expressions, field typing, null handling, casing, and whether application filters match stored metadata.

**Smallest safe fix**  
Start from no filter, then re-add conditions one by one. Remove any filter acting as a hidden hard gate.

**How to prove it**  
Compare top results with no filter, then with each filter layer enabled, and identify where recall drops.

**Often confused with**  
[No.8](#no8), because routing to the wrong partition can look like filter failure.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no10"></a>

### No.10 Index or search parameter mismatch

**What you see**  
Ranking quality and latency swing across runs, environments, or dataset changes.

**What it usually means**  
Index type or search parameters are poorly matched to the dataset size, vector distribution, or recall target.

**What to inspect in Milvus**  
Inspect index configuration, search parameters, recall targets, and whether the same configuration is used consistently across environments.

**Smallest safe fix**  
Tune index and search parameters against a fixed validation set instead of changing them ad hoc in production.

**How to prove it**  
Record recall and latency on the same query set before and after tuning. Keep the new setting only if both are acceptable.

**Often confused with**  
[No.4](#no4), because metric mismatch can also create unstable ranking behavior.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no11"></a>

### No.11 Candidate starvation

**What you see**  
The answer feels under-informed because too few useful candidates make it into the later stages.

**What it usually means**  
Top-k is too small, pre-filters are too aggressive, or reranking receives an already starved candidate set.

**What to inspect in Milvus**  
Inspect raw retrieval candidate count, application side cutoffs, and the number of candidates handed into reranking or answer synthesis.

**Smallest safe fix**  
Increase the candidate pool before later ranking stages. Do not try to repair a starved candidate set after the fact.

**How to prove it**  
Increase the pool on a fixed query set and confirm that missing evidence now appears.

**Often confused with**  
[No.2](#no2), because poor chunking can also hide the answer-bearing unit.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no12"></a>

### No.12 Duplicate and near duplicate collapse

**What you see**  
Top results are filled with repeated or near-identical chunks, leaving little evidence diversity.

**What it usually means**  
The store contains duplicate inserts, version drift, or chunking logic that creates many nearly identical vectors.

**What to inspect in Milvus**  
Inspect duplicate IDs, repeated ingestion of the same source, and overlap patterns that generate near-identical chunks.

**Smallest safe fix**  
Deduplicate at ingestion time and apply lightweight diversity control before answer assembly.

**How to prove it**  
Re-run a fixed query and confirm that top results now cover distinct evidence instead of repeated clones.

**Often confused with**  
[No.11](#no11), because a tiny candidate pool can also make evidence look narrow, even if it is not duplicated.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

### Stage 3 summary

If retrieval improves when filters are removed or top-k is widened, stay in Stage 3.  
Only tune parameters after you confirm storage truth and embedding alignment are already correct.

## Stage 4. Grounding and answer assembly

<a id="no13"></a>

### No.13 Context packing disorder

**What you see**  
Relevant evidence is retrieved, but the final answer still misses it, misreads it, or gives weak grounding.

**What it usually means**  
The answer stage receives chunks in a poor order, with weak separators, missing labels, or harmful truncation.

**What to inspect in Milvus**  
Inspect how retrieved chunks are ordered, labeled, truncated, and packed into the final prompt.

**Smallest safe fix**  
Pack context in a stable order, keep source labels visible, and place the strongest evidence where the model can see it clearly.

**How to prove it**  
Inspect the exact final prompt sent to the answer model and verify that the best evidence is visible and clearly separated.

**Often confused with**  
[No.1](#no1), because off-target answers can come from either bad retrieval intent or bad context assembly.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no14"></a>

### No.14 Cross document contamination

**What you see**  
The final answer blends facts from different documents, different versions, or different tenants as if they were one source.

**What it usually means**  
Retrieved evidence crosses incompatible boundaries, and the answer stage merges it without preserving provenance.

**What to inspect in Milvus**  
Inspect whether retrieved chunks come from conflicting sources and whether the prompt explicitly marks source identity.

**Smallest safe fix**  
Group evidence by source, version, or tenant before answer synthesis. Prevent incompatible chunks from being treated as one record.

**How to prove it**  
Use a conflict case where two sources disagree and confirm the answer preserves the boundary instead of blending them.

**Often confused with**  
[No.7](#no7), because stale content that should have been removed can also create apparent source conflicts.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no15"></a>

### No.15 Citation and provenance loss

**What you see**  
The answer may sound correct, but the user cannot reliably tell where claims came from.

**What it usually means**  
Metadata, source identifiers, or chunk references are dropped between retrieval and final answer formatting.

**What to inspect in Milvus**  
Inspect whether document ID, chunk ID, title, section, and timestamp survive from storage to final output formatting.

**Smallest safe fix**  
Carry provenance fields through the entire pipeline and require answer generation to cite only retrieved evidence.

**How to prove it**  
Inspect several answers and confirm every cited claim maps back to a real retrieved chunk.

**Often confused with**  
[No.13](#no13), because messy context packing can also weaken visible grounding.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

<a id="no16"></a>

### No.16 Verification gap

**What you see**  
A change looks better once, but the team cannot tell whether the system actually improved.

**What it usually means**  
Fixes are judged by anecdotes instead of a stable benchmark and a repeatable before versus after workflow.

**What to inspect in Milvus**  
Inspect whether the team has a fixed query set, expected outcomes, and a simple comparison routine for retrieval changes.

**Smallest safe fix**  
Create a small locked benchmark before making more retrieval changes. Evaluate against the same benchmark every time.

**How to prove it**  
Accept a change only if the same benchmark shows measurable improvement without introducing new regressions.

**Often confused with**  
[No.10](#no10), because unstable parameters can create inconsistent results that look like evaluation noise.

[Back to symptom navigator](#symptom-navigator) | [Back to quick index](#quick-index)

### Stage 4 summary

If retrieval is already correct but the final answer still blends, drops, or obscures evidence, stay in Stage 4.  
Do not keep tuning retrieval if the real issue is in grounding, provenance, or evaluation discipline.

## Milvus first repair order

When debugging Milvus based RAG, this is the safest order to work through:

1. Schema and vector dimension
2. Embedding contract consistency
3. Metric and normalization alignment
4. Collection or partition routing
5. Ingestion completeness
6. Update and delete visibility
7. Filter behavior
8. Search parameter tuning
9. Candidate pool size
10. Final grounding and citation retention

## When this page is not the right tool

This page is not the first place to start if:

- retrieval is already correct and the issue is purely model reasoning quality
- the failure is caused entirely by application business rules after retrieval
- the behavior cannot be reproduced with a fixed query set
- the issue is mainly about SDK usage, API syntax, or deployment setup rather than retrieval quality

## Credit

This checklist is adapted from the open source WFGY 16 problem diagnostic map and rewritten here in a Milvus focused operational form.
