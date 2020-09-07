---
id: milvus_distributions-cpu.md
label: CPU 版 Milvus
order: 0
group: distribution
---

# Milvus 版本比较

## 概述

{{fragments/distributions.md}}

{{tab}} 


## CPU 版 Milvus 支持的索引类型

<div class="filter">
<a href="#floating">浮点型向量</a> <a href="#binary">二值型向量</a>
{{fragments/choose_embedding_type.md}}
</div>

<div class="filter-floating table-wrapper" markdown="block">

| 索引类型  | CPU 建索引        | GPU 建索引      |  CPU 搜索           | GPU 搜索        |
| -------- | ----------------- | -------------- | ------------------- | --------------- |
| FLAT     | N/A               |   N/A          |    ✔️               | ❌              |
| IVF_FLAT | ✔️                |  ❌           |    ✔️               | ❌              |
| IVF_SQ8  | ✔️                |  ❌           |    ✔️               | ❌              |
| IVF_PQ   | ✔️                |  ❌           |    ✔️               | ❌              |
| RNSG     | ✔️                |  ❌           |    ✔️               | ❌              |
| HNSW     | ✔️                |  ❌           |    ✔️               | ❌              |
| ANNOY    | ✔️                |  ❌           |    ✔️               | ❌              |

</div>

<div class="filter-binary table-wrapper" markdown="block">

| 索引类型  | CPU 建索引        | GPU 建索引       |  CPU 搜索            | GPU 搜索        |
| -------- | ----------------- | --------------  | -------------------- | --------------- |
| FLAT     | N/A               | N/A             | ✔️                  | ❌              |
| IVF_FLAT | ✔️                | ❌             | ✔️                  | ❌              |

</div>
