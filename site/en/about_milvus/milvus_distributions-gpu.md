---
id: milvus_distributions-gpu.md
label: GPU-only Milvus
order: 1
group: distribution
---

# Milvus Distributions

{{tab}} 

## Overview

{{fragments/distributions.md}}


## Indexes for GPU-enabled Milvus

<div class="table-wrapper" markdown="block">

| Name       | Index building with CPU | Search with CPU | Search with GPU                                                  | Search with GPU                                          | Float vector support | Binary vector support |
| ---------- | ----------------------- | --------------- | ---------------------------------------------------------------- | -------------------------------------------------------- | -------------------- | --------------------- |
| FLAT     | -                | ✔️            | -                  | ✔️<br>(Only Supports floating point vectors) | ✔️             | ✔️            |
| IVF_FLAT | ✔️                | ✔️            | ✔️<br>(Only Supports floating point vectors)  | ✔️<br>(Only Supports floating point vectors) | ✔️             | ✔️            |
| IVF_SQ8  | ✔️                | ✔️            | ✔️                  | ✔️                 | ✔️             | ❌           |
| IVF_SQ8H | ✔️                | ✔️            | ✔️                  | ✔️                 | ✔️             | ❌           |
| IVF_PQ   | ✔️                | ✔️            | ✔️<br>(Only Supports GPU index for Euclidean distance)                  | ✔️<br>(Only Supports GPU search for Euclidean distance)                 | ✔️             | ❌           |
| RNSG     | ✔️                | ✔️            | ❌                 | ❌                | ✔️             | ❌           |
| HNSW     | ✔️                | ✔️            | ❌                 | ❌                | ✔️             | ❌           |
| ANNOY    | ✔️                | ✔️            | ❌                 | ❌                | ✔️             | ❌           |

</div>

<div class="alert note">
<ul>
<li>For indexes supporting both CPU search and GPU search, you can create or search them using different devices, either CPU or GPU. For example, you can create an index using CPU and conduct a vector search using GPU.</li>
</ul>
</div>