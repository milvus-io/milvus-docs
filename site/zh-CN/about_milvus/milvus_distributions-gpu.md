---
id: milvus_distributions-gpu.md
label: GPU 版 Milvus
order: 1
group: distribution
---

# Milvus 版本比较

{{tab}} 

## 概述

{{fragments/distributions.md}}


## GPU 版本 Milvus 支持的索引类型

<div class="filter">
<a href="#floating">浮点型向量</a> <a href="#binary">二值型向量</a>
</div>

<div class="filter-floating table-wrapper" markdown="block">

| 索引类型  | CPU 建索引        | CPU 搜索       | GPU 建索引           | GPU 搜索         |
| -------- | ----------------- | ------------- | -------------------- | --------------- |
| FLAT     | N/A                | ✔️            | N/A                  | ✔️            |
| IVF_FLAT | ✔️                | ✔️            | ✔️                  | ✔️             |
| IVF_SQ8  | ✔️                | ✔️            | ✔️                  | ✔️             |
| IVF_SQ8H | ✔️                | ✔️            | ✔️                  | ✔️             |
| IVF_PQ   | ✔️                | ✔️            | ✔️                  | ✔️             |
| RNSG     | ✔️                | ✔️            | ❌                 | ❌              |
| HNSW     | ✔️                | ✔️            | ❌                 | ❌              |
| ANNOY    | ✔️                | ✔️            | ❌                 | ❌              |

</div>


<div class="filter-binary table-wrapper" markdown="block">

| 索引类型  | CPU 建索引        | CPU 搜索       | GPU 建索引           | GPU 搜索        |
| --------- | ---------------- | -------------- | ------------------- | --------------- |
| FLAT       | N/A              | ✔️            | N/A                 | ❌             |
| IVF_FLAT   | ✔️              | ✔️             | ❌                 | ❌             |

</div>
<div class="alert note">
对于那些 CPU 和 GPU 同时支持的索引，Milvus 支持在创建和搜索时使用不同的设备。比如，你可以在 GPU 上创建索引后再在 CPU 上查询，也可以在 CPU 上创建索引后再在 GPU 上查询。
</div>