---
id: milvus_distributions-cpu.md
label: CPU-only Milvus
order: 0
group: distribution
---

# Milvus Distributions

{{tab}} 

## Overview


{{fragments/distributions.md}}



## Indexes for CPU-only Milvus

<div class="table-wrapper" markdown="block">

| Name       | Index building with CPU | Search with CPU | Float vector support | Binary vector support |
| -------- | ----------------- | -------------- | -------------- | ---------------- |
| FLAT     | -                 | ✔️             | ✔️             | ✔️         　   |
| IVF_FLAT | ✔️                | ✔️            | ✔️             | ✔️          　  |
| IVF_SQ8  | ✔️                | ✔️            | ✔️             | ❌             |
| IVF_PQ   | ✔️                | ✔️            | ✔️             | ❌             |
| RNSG     | ✔️                | ✔️            | ✔️             | ❌             |
| HNSW     | ✔️                | ✔️            | ✔️             | ❌             |
| ANNOY    | ✔️                | ✔️            | ✔️             | ❌             |

</div>

