---
id: milvus_distributions-gpu.md
label: GPU 版 Milvus
order: 1
group: distribution
---

# Milvus 版本比较

## 概述

{{fragments/distributions.md}}

{{tab}} 


## GPU 版 Milvus 支持的索引类型

{{fragments/choose_embedding_type.md}}

<div class="filter">
<a href="#floating">浮点型向量</a> <a href="#binary">二值型向量</a>

</div>

<div class="filter-floating table-wrapper" markdown="block">

| 索引类型  | CPU 建索引        | GPU 建索引      | CPU 搜索            | GPU 搜索         |
| -------- | ----------------- | -------------  | -------------------- | --------------- |
| FLAT     | N/A                | N/A           | ✔️                  | ✔️            |
| IVF_FLAT | ✔️                | ✔️            | ✔️                  | ✔️             |
| IVF_SQ8  | ✔️                | ✔️            | ✔️                  | ✔️             |
| IVF_SQ8H | ✔️                | ✔️            | ✔️                  | ✔️             |
| IVF_PQ   | ✔️                | ✔️            | ✔️                  | ✔️             |
| RNSG     | ✔️                | ❌            | ✔️                  | ❌              |
| HNSW     | ✔️                | ❌            | ✔️                  | ❌              |
| ANNOY    | ✔️                | ❌            | ✔️                  | ❌              |

<div class="alert note">
CPU 和 GPU 创建的索引完全一致，只是一般情况下 GPU 的创建索引速度快于 CPU 的创建速度。
</div>
</div>


<div class="filter-binary table-wrapper" markdown="block">

| 索引类型  | CPU 建索引        | GPU 建索引      | CPU 搜索            | GPU 搜索        |
| --------- | ---------------- | -------------- | ------------------- | --------------- |
| FLAT       | N/A             | N/A            | ✔️                 | ❌             |
| IVF_FLAT   | ✔️              | ❌            | ✔️                 | ❌             |

</div>
