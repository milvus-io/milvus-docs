---
id: milvus_distributions-gpu.md
label: GPU-enabled Milvus
order: 1
group: distribution
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
| ANNOY    | ✔️                | ❌                 | ✔️                  | ❌              |

<div class="alert note">
<ul>
<li>For indexes supporting both CPU and GPU, you can create or search them using different devices. For example, you can create an index using CPU and conduct a vector search using GPU, and vice versa.</li>
</ul>
</div>
</div>

<div class="filter-binary table-wrapper" markdown="block">

| Index type | Indexing with CPU | Indexing with GPU | Search with CPU    | Search with GPU |
| ---------- | ----------------- | ----------------  | ------------------ | --------------- |
| FLAT       | N/A               | N/A               | ✔️                 | ❌             |
| IVF_FLAT   | ✔️                | ❌               | ✔️                 | ❌             |


</div>

