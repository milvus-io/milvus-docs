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
| Annoy    | ✔️                | ❌            | ✔️                  | ❌              |

<div class="alert note">
<ul>
<li>CPU 和 GPU 创建的索引完全一致，只是一般情况下 GPU 的创建索引速度快于 CPU 的创建速度。</li>
<li><code>top_k</code> > 2048 时，Milvus 由 GPU 查询切换为 CPU 查询。</li>
<li><code>nprobe</code> > 2048 时，Milvus 由 GPU 查询切换为 CPU 查询。</li>
</ul>
</div>
</div>


<div class="filter-binary table-wrapper" markdown="block">

| 索引类型  | CPU 建索引        | GPU 建索引      | CPU 搜索            | GPU 搜索        |
| --------- | ---------------- | -------------- | ------------------- | --------------- |
| FLAT       | N/A             | N/A            | ✔️                 | ❌             |
| IVF_FLAT   | ✔️              | ❌            | ✔️                 | ❌             |

</div>


