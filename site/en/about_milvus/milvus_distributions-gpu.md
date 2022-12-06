---
id: milvus_distributions-gpu.md
label: GPU-enabled Milvus
order: 1
group: distribution
summary: Learn about the indexes supported for GPU-enabled Milvus.
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
| IVF_FLAT | ✔️                | ✔️                 | ✔️                  | ✔️              |
| IVF_SQ8  | ✔️                | ✔️                 | ✔️                  | ✔️              |
| IVF_SQ8H | ✔️                | ✔️                 | ✔️                  | ✔️              |
| IVF_PQ   | ✔️                | ✔️                 | ✔️                  | ✔️              |
| RNSG     | ✔️                | ❌                 | ✔️                  | ❌              |
| HNSW     | ✔️                | ❌                 | ✔️                  | ❌              |
| Annoy    | ✔️                | ❌                 | ✔️                  | ❌              |


<div class="alert note">
<ul>
<li>An index built with GPU is identical to built with CPU. The only difference is the time to build the index: GPU usually takes less time.</li>
<li>If <code>top_k</code> > 2048, Milvus switches from GPU search to CPU search.</li>
<li>If <code>nprobe</code> > 2048, Milvus switches from GPU search to CPU search.</li>
</ul>
</div>

</div>

<div class="filter-binary table-wrapper" markdown="block">

| Index type | Indexing with CPU | Indexing with GPU | Search with CPU    | Search with GPU |
| ---------- | ----------------- | ----------------  | ------------------ | --------------- |
| FLAT       | N/A               | N/A               | ✔️                 | ❌             |
| IVF_FLAT   | ✔️                | ❌               | ✔️                 | ❌             |


</div>

