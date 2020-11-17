---
id: milvus_distributions-gpu.md
label: GPU-enabled Milvus
order: 1
group: distribution
icon: tab-icon-gpu
---

# Milvus Distributions

## Overview

{{fragments/distributions.md}}

{{tab}} 

## Indexes for GPU-enabled Milvus

{{fragments/choose_embedding_type.md}}

<div class="filter">
<a href="#floating">Floating point embeddings</a> <a href="#binary">Binary embeddings</a>

</div>

<div class="filter-floating table-wrapper" markdown="block">

| Index type | Indexing with CPU | Indexing with GPU |  Search with CPU     | Search with GPU |
| ---------- | ----------------- | ----------------- | -------------------- | --------------- |
| FLAT     | N/A                | N/A                | ✔️                  | ✔️              |
| IVF\_FLAT | ✔️                | ✔️                 | ✔️                  | ✔️              |
| IVF\_SQ8  | ✔️                | ✔️                 | ✔️                  | ✔️              |
| IVF\_SQ8H | ✔️                | ✔️                 | ✔️                  | ✔️              |
| IVF\_PQ   | ✔️                | ✔️                 | ✔️                  | ✔️              |
| RNSG     | ✔️                | ❌                 | ✔️                  | ❌              |
| HNSW     | ✔️                | ❌                 | ✔️                  | ❌              |
| ANNOY    | ✔️                | ❌                 | ✔️                  | ❌              |


<div class="alert note">
<ul>
<li>An index built with GPU is identical to that built with CPU. The only difference is that GPU usually takes less time to build index.</li>
<li>If <code>top_k</code> > 2048, Milvus switches from GPU search to CPU search.</li>
<li>If <code>nprobe</code> > 2048, Milvus switches from GPU search to CPU search.</li>
</ul>
</div>

</div>

<div class="filter-binary table-wrapper" markdown="block">

| Index type | Indexing with CPU | Indexing with GPU | Search with CPU    | Search with GPU |
| ---------- | ----------------- | ----------------  | ------------------ | --------------- |
| BIN\_FLAT       | N/A               | N/A               | ✔️                 | ❌             |
| BIN\_IVF_FLAT   | ✔️                | ❌               | ✔️                 | ❌             |


</div>

