---
id: create_drop_index_python.md
---

# 创建、删除索引

本页提供创建或删除索引的 Python 示例代码。

## 创建索引

目前，一个集合只支持一种索引类型，切换索引类型会自动删除旧的索引文件。在创建其它索引前，FLAT 作为集合的默认索引类型。

<div class="alert note">
<code>create_index()</code> 会指定该集合的索引类型，并同步为之前插入的数据建立索引，后续插入的数据在大小达到 <code>index_file_size</code> 时，索引会在后台自动建立。在实际生产环境中，如果是流式数据，建议在插入向量之前先创建索引，以便后续系统自动建立；如果是静态数据，建议导入所有数据后再一次性创建索引。更多索引用法请参考 <a href="https://github.com/milvus-io/pymilvus/tree/master/examples/indexes">索引示例程序</a>。
</div>

1. 准备创建索引所需参数（以 `IVF_FLAT` 为例）。索引参数是一个 JSON 字符串，在 Python SDK 中以字典来表示。

   ```python
   # Prepare index param.
   >>> ivf_param = {'nlist': 16384}
   ```

   <div class="alert note">
   对于不同的索引类型，创建索引所需参数也有区别。所有的索引参数都<b>必须赋值</b>。
   </div>

   | 索引类型          | 索引参数    | 示例参数      | 取值范围  |
   | ----------------| ------------| ------------- | --------------------------------- |
   | `IVF_FLAT` / `IVF_SQ8`/ `IVF_SQ8H` | `nlist`：建立索引时对向量数据文件进行聚类运算的分簇数。索引文件会记录聚类运算后的结果，包括索引的类型，每个簇的中心向量，以及每个簇分别有哪些向量，以便于后期搜索。    | `{nlist: 16384}`   | `nlist`：[1, 65536]       |
   | `IVF_PQ`    | `nlist`：建立索引时对向量数据文件进行聚类运算的分簇数。索引文件会记录聚类运算后的结果，包括索引的类型，每个簇的中心向量，以及每个簇分别有哪些向量，以便于后期搜索。 </br></br> `m`：建立索引时数据的压缩率。m 越小压缩率越高。             | `{nlist: 16384, m: 12}`                                                 | `nlist`：[1, 65536] </br></br> `m`: {96, 64, 56, 48, 40, 32, 28, 24, 20, 16, 12, 8, 4, 3, 2, 1} 中的值，并且分解出的低维向量空间的维度须在 {1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32} 内。此外，用 GPU 计算时，m x 1024 的值还不能超过显卡的 MaxSharedMemPerBlock。                             |
   | `RNSG`    | `search_length`：值越大，代表在图中搜索的节点越多，召回率越高，但速度也越慢。建议 `search_length` 小于 `candidate_pool` 的值，取值范围建议在 [40, 80]。</br></br> `out_degree`：值越大，则占用内存越大，搜索性能也越好。</br></br> `candidate_pool`：影响索引质量，建议取值范围 [200,500]。</br></br> `knng`：影响索引质量，建议取值为 `out_degree` + 20。 | `{search_length: 45, out_degree:50, candidate_pool_size:300, knng:100}` | `search_length`: [10, 300]</br></br>`out_degree`: [5, 300]</br></br>`candidate_pool_size`: [50, 1000]</br></br>`knng`: [5, 300] |
   | `HNSW`                            | `M`：影响 build 的时间以及索引的质量。 `M` 越大，构建索引耗时越长，索引质量越高，内存占用也越大。 </br></br> `efConstruction`：影响 build 的时间以及索引的质量。 `efConstruction` 越大，构建索引耗时越长，索引质量越高，内存占用也越大。                                                                                                             | `{M: 16, efConstruction: 500}`                                           | `M`: [4, 64]</br></br>`efConstruction`: [8, 512]                                                                             |
   | `ANNOY`                           | `n_trees`: 影响建立索引的时间和索引大小。值越大，搜索结果越精确，但索引越大。                   | `{n_trees: 8}`                                                      |  [1, 1024]                    |

   详细信息请参考 [Milvus 索引类型](index.md)。

2. 为指定集合创建索引：

   ```python
   # Create an index.
   >>> milvus.create_index('test01', IndexType.IVF_FLAT, ivf_param)
   ```

## 删除索引

删除索引后，集合再次使用默认索引类型 FLAT。

```python
>>> milvus.drop_index('test01')
```

## 常见问题

<details>
<summary><font color="#3f9cd1">建索引参数 <code>nlist</code> 的大小该如何选择？</font></summary>
{{fragments/faq_set_nlist.md}}
</details>
<details>
<summary><font color="#3f9cd1">Milvus 可以在同一个集合中的不同分区上建立不同索引吗？</font></summary>
{{fragments/faq_collection_different_index.md}}
</details>
<details>
<summary><font color="#3f9cd1">Milvus 中支持新增向量后再建索引吗？</font></summary>
{{fragments/faq_create_index_after_insertion.md}}
</details>

