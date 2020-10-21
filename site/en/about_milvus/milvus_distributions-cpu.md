---
id: milvus_distributions-cpu.md
label: CPU-only Milvus
order: 0
group: distribution
---

# Milvus Distributions



## Overview


{{fragments/distributions.md}}

{{tab}} 

## Indexes for CPU-only Milvus

{{fragments/choose_embedding_type.md}}

<div class="filter">
<a href="#floating">Floating point embeddings</a> <a href="#binary">Binary embeddings</a>

</div>

<div class="filter-floating table-wrapper" markdown="block">

| Index type | Indexing with CPU | Indexing with GPU | Search with CPU          | Search with GPU |
| ---------- | ----------------- | ----------------- | ------------------------ | --------------- |
| FLAT       | N/A               | N/A               | ✔️                      | ❌              |
| IVF\_FLAT   | ✔️                | ❌               | ✔️                      | ❌              |
| IV\_SQ8    | ✔️                | ❌               | ✔️                      | ❌              |
| IVF\_PQ     | ✔️                | ❌               | ✔️                      | ❌              |
| RNSG       | ✔️                | ❌               | ✔️                      | ❌              |
| HNSW       | ✔️                | ❌               | ✔️                      | ❌              |
| ANNOY      | ✔️                | ❌               | ✔️                      | ❌              |

</div>

<div class="filter-binary table-wrapper" markdown="block">

| Index type | Indexing with CPU | Indexing with GPU | Search with CPU       | Search with GPU |
| ---------- | ----------------------- | ----------------- | --------------------- | --------------- |
| BIN\_FLAT       | N/A                     |  N/A              | ✔️                    | ❌              |
| BIN\_IVF\_FLAT   | ✔️                      | ❌               | ✔️                    | ❌              |

</div>

