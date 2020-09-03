---
id: milvus_distributions.md
---

# Milvus 版本比较

{{fragments/distributions.md}}


## CPU 版本 Milvus 支持的索引类型

<div class="table-wrapper" markdown="block">

| 索引类型    | CPU 建索引 | CPU 搜索 | 浮点型向量 | 二值型向量 |
| ---------- | ---------------- | ------------ | ------------- | ------------- |
| FLAT     | N/A                | ✔️            | ✔️             | ✔️         　   |
| IVF_FLAT | ✔️                | ✔️            | ✔️             | ✔️          　  |
| IVF_SQ8  | ✔️                | ✔️            | ✔️             | ❌             |
| IVF_PQ   | ✔️                | ✔️            | ✔️             | ❌             |
| RNSG     | ✔️                | ✔️            | ✔️             | ❌             |
| HNSW     | ✔️                | ✔️            | ✔️             | ❌             |
| ANNOY    | ✔️                | ✔️            | ✔️             | ❌             |

</div>

## GPU 版本 Milvus 支持的索引类型

<div class="table-wrapper" markdown="block">

| 索引类型    | CPU 建索引    | CPU 搜索 | GPU 建索引      | GPU 搜索       | 浮点型向量  | 二值型向量 |
| ---------- | ---------------- | ------------ | ------------------ | ----------------- | ------------- | ------------ |
| FLAT     | N/A                | ✔️            | N/A                  | ✔️<br>（仅支持浮点型向量） | ✔️             | ✔️            |
| IVF_FLAT | ✔️                | ✔️            | ✔️<br>（仅支持浮点型向量）  | ✔️<br>（仅支持浮点型向量） | ✔️             | ✔️            |
| IVF_SQ8  | ✔️                | ✔️            | ✔️                  | ✔️                 | ✔️             | ❌           |
| IVF_SQ8H | ✔️                | ✔️            | ✔️                  | ✔️                 | ✔️             | ❌           |
| IVF_PQ   | ✔️                | ✔️            | ✔️<br>（仅对欧氏距离支持 GPU 索引）                  | ✔️<br>（仅对欧氏距离支持 GPU 搜索）                 | ✔️             | ❌           |
| RNSG     | ✔️                | ✔️            | ❌                 | ❌                | ✔️             | ❌           |
| HNSW     | ✔️                | ✔️            | ❌                 | ❌                | ✔️             | ❌           |
| ANNOY    | ✔️                | ✔️            | ❌                 | ❌                | ✔️             | ❌           |

</div>

<div class="alert note">
<ul>
<li>对于那些 CPU 和 GPU 同时支持的索引，Milvus 支持在创建和搜索时使用不同的设备。比如，你可以在 GPU 上创建索引后再在 CPU 上查询，也可以在 CPU 上创建索引后再在 GPU 上查询。</li>
</ul>
</div>