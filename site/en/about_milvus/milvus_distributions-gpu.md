---
id: milvus_distributions-gpu.md
label: GPU-enabled Milvus
order: 1
group: distribution
---

# Milvus Distributions

{{tab}} 

## Overview

{{fragments/distributions.md}}


## Indexes for GPU-enabled Milvus

<div class="filter">
<a href="#floating">Floating point embeddings</a> <a href="#binary">Binary embeddings</a>
</div>

<div class="table-wrapper filter-floating" markdown="block">

| Index type | Indexing with CPU | Search with CPU | Indexing with GPU         | Search with GPU |
| ---------- | ----------------- | --------------- | ------------------------- | --------------- |
| FLAT     | N/A                | ✔️            | N/A                  | ✔️                    |
| IVF_FLAT | ✔️                | ✔️            | ✔️                  | ✔️                 |
| IVF_SQ8  | ✔️                | ✔️            | ✔️                  | ✔️                 |
| IVF_SQ8H | ✔️                | ✔️            | ✔️                  | ✔️                 |
| IVF_PQ   | ✔️                | ✔️            | ✔️                  | ✔️                |
| RNSG     | ✔️                | ✔️            | ❌                 | ❌                |
| HNSW     | ✔️                | ✔️            | ❌                 | ❌                |
| ANNOY    | ✔️                | ✔️            | ❌                 | ❌                |

</div>

<div class="table-wrapper filter-binary" markdown="block">

| Index type | Indexing with CPU | Search with CPU | Indexing with GPU  | Search with GPU |
| ---------- | ----------------- | --------------- | ------------------ | --------------- |
| FLAT       | N/A                | ✔️             | N/A                | ❌             |
| IVF_FLAT   | ✔️                | ✔️             | ❌                 | ❌             |


</div>

<div class="alert note">
<ul>
<li>For indexes supporting both CPU search and GPU search, you can create or search them using different devices, either CPU or GPU. For example, you can create an index using CPU and conduct a vector search using GPU.</li>
</ul>
</div>