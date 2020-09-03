---
id: milvus_distributions-cpu.md
label: CPU 版 Milvus
order: 0
group: distribution
---

# Milvus 版本比较

{{tab}} 

## 概述

{{fragments/distributions.md}}


## CPU 版本 Milvus 支持的索引类型

<div class="filter">
<a href="#floating">浮点型向量</a> <a href="#binary">二值型向量</a>
</div>

<div class="table-wrapper filter-floating" markdown="block">

| 索引类型  | CPU 建索引        | CPU 搜索       |
| -------- | ----------------- | -------------- |
| FLAT     | N/A                | ✔️           |
| IVF_FLAT | ✔️                | ✔️            |
| IVF_SQ8  | ✔️                | ✔️            |
| IVF_PQ   | ✔️                | ✔️            |
| RNSG     | ✔️                | ✔️            |
| HNSW     | ✔️                | ✔️            |
| ANNOY    | ✔️                | ✔️            |

</div>

<div class="table-wrapper filter-binary" markdown="block">

| 索引类型  | CPU 建索引        | CPU 搜索        |
| -------- | ----------------- | -------------- |
| FLAT     | N/A               | ✔️             |
| IVF_FLAT | ✔️                | ✔️            |

</div>

<div class="alert note">
<ul>
<li>对于那些 CPU 和 GPU 同时支持的索引，Milvus 支持在创建和搜索时使用不同的设备。比如，你可以在 GPU 上创建索引后再在 CPU 上查询，也可以在 CPU 上创建索引后再在 GPU 上查询。</li>
</ul>
</div>