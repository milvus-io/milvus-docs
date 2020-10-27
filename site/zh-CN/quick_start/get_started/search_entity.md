---
id: search_entity.md
---

# 查询向量

Milvus 支持在集合或分区中查询向量。

## 在集合中查询向量

1. 创建搜索参数 DSL。

   ```python
   # This DSL searches for topk `entities` that are
   # closest to vectors[:1] searched by `IVF_FLAT` index with `nprobe = 10` and `metric_type = L2`,
   # AND field "A" in [1, 2, 5],
   # AND field "B" greater than 1 less than 100
   >>> dsl = {
   ...     "bool": {
   ...         "must":[
   ...             {
   ...                 "term": {"A": [1, 2, 5]}
   ...             },
   ...             {
   ...                 "range": {"B": {"GT": 1, "LT": 100}}
   ...             },
   ...             {
   ...                 "vector": {
   ...                    "Vec": {"topk": 10, "query": vectors[:1], "metric_type": "L2", "params": {"nprobe": 10}}
   ...                 }
   ...             }
   ...         ]
   ...     }
   ... }
   ```

   <div class="alert note">
   <ul>
   <li><code>top_k</code> 指的是向量空间中距离目标向量最近的 k 个向量。</li>
   <li><code>top_k</code> 的范围为：[1, 16384]。</li>
   <li>对于不同的索引类型，搜索所需参数也有区别。所有的搜索参数都<b>必须赋值</b>。详细信息请参考 <a href="index.md">Milvus 索引类型</a>。</li>
   </ul>
   </div>

2. 进行搜索：

   ```python
   >>> client.search('test01', dsl)
   ```

   你也可以指定搜索结果中返回指定列的值，此处我们获取字段 `B` 的值：

   ```python
   >>> client.search('test01', dsl, fields=["B"])
   ```

## 在分区中查询向量

```python
>>> client.search('test01', dsl, partition_tags=['tag01'])
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
