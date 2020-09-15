---
id: search_vector_python.md
---

# 查询向量

Milvus 支持在集合或分区中查询向量。

## 在集合中查询向量

1. 创建搜索参数。搜索参数是一个 JSON 字符串，在 Python SDK 中以字典来表示。

   ```python
   >>> search_param = {'nprobe': 16}
   ```

   <div class="alert note">
   对于不同的索引类型，搜索所需参数也有区别。所有的搜索参数都<b>必须赋值</b>。
   </div>

   | 索引类型                             | 搜索参数                                                                                    | 示例参数              | 取值范围       |
   | ------------------------------------ | ------------------------------------------------------------------------------------------- | --------------------- | -------------- |
   | FLAT | - | | - |
   | IVF\_FLAT / IVF\_SQ8 / IVF\_SQ8H / IVF\_PQ | `nprobe`：查询时所涉及的向量类的个数。`nprobe` 影响查询精度。数值越大，精度越高，速度越慢。         | `{nprobe: 32}`         | CPU: [1, nlist] </br> GPU: [1, min(2048, nlist)]   |
   | RNSG                                | `search_length`：值越大，代表在图中搜索的节点越多，召回率越高，速度越慢。                         | `{search_length: 100}` | [10, 300]      |
   | HNSW                               | `ef`：值越大，则在索引中搜索的数据越多，召回率越高，速度越慢。                                    | `{ef: 64}`            | [`top_k`, 4096] |
   | ANNOY                              | `search_k`: 影响搜索性能。值越大，搜索结果越精确，但搜索时间越长。</br>-1 表示默认值，取总数据量的5%。 | `{search_k: -1}`    | {-1} ∪ [`top_k`, n × n_trees] |

   <div class="alert note">
   <code>top_k</code> 是与目标向量最相似的 k 条向量，在搜索时定义。<code>top_k</code> 的取值范围是 (0, 2048]。
   </div>

2. 创建随机向量作为 `query_records` 进行搜索：

   ```python
   # Create 5 vectors of 256 dimensions.
   >>> q_records = [[random.random() for _ in range(256)] for _ in range(5)]
   >>> milvus.search(collection_name='test01', query_records=q_records, top_k=2, params=search_param)
   ```

## 在分区中查询向量

```python
# Create 5 vectors of 256 dimensions.
>>> q_records = [[random.random() for _ in range(256)] for _ in range(5)]
>>> milvus.search(collection_name='test01', query_records=q_records, top_k=1, partition_tags=['tag01'], params=search_param)
```

<div class="alert note">
如果你不指定 <code>partition_tags</code>， Milvus 会在整个集合中搜索。
</div>


## 常见问题

<details>
<summary><font color="#4fc4f9">为什么 Milvus 查询召回率一直不理想？</font></summary>
{{fragments/faq_poor_recall_rate.md}}
</details>
<details>
<summary><font color="#4fc4f9">Milvus 是否支持 “边插入边查询” ？</font></summary>
{{fragments/faq_search_during_insert.md}}
</details>
<details>
<summary><font color="#4fc4f9">对集合分区的查询是否会受到集合大小的影响，尤其在集合数据量高达一亿数据量时？</font></summary>
{{fragments/faq_collection_affect_partition_search.md}}
</details>
<details>
<summary><font color="#4fc4f9">如果只是搜索集合中的部分分区，整个集合的数据会全部加载到内存吗？</font></summary>
{{fragments/faq_load_when_search_partition.md}}
</details>
<details>
<summary><font color="#4fc4f9">各个数据段的检索是并行处理的吗？</font></summary>
{{fragments/faq_search_segment_parallel.md}}
</details>
<details>
<summary><font color="#4fc4f9">批量搜索时，用多线程的收益大吗？</font></summary>
{{fragments/faq_multithreading_search.md}}
</details>
<details>
<summary><font color="#4fc4f9">为什么搜索的速度非常慢？</font></summary>
{{fragments/faq_search_slow.md}}
</details>
<details>
<summary><font color="#4fc4f9">创建索引立即查询，为什么内存会突然增长？</font></summary>
{{fragments/faq_search_increase_memory_usage.md}}
</details>
<details>
<summary><font color="#4fc4f9">为什么重启 Milvus 服务端之后，第一次搜索时间非常长？</font></summary>
{{fragments/faq_search_time_after_restart.md}}
</details>
