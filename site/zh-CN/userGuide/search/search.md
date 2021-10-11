---
id: search.md
---

# 查询向量
通过本章节文档，你将了解如何在 Milvus 中进行相似性搜索。

1. 创建搜索参数：

{{fragments/multiple_code.md}}

```python
>>> search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
```

```javascript
const searchParams = {
  anns_field: "example_field",
  topk: "4",
  metric_type: "L2",
  params: JSON.stringify({ nprobe: 10 }),
};
```

2. 在查询向量前，将集合加载到内存中：

{{fragments/multiple_code.md}}

```python
>>> collection.load()
```

```javascript
await milvusClient.collectionManager.loadCollection({
  collection_name: COLLECTION_NAME,
});
```
<div class="alert warning">
在当前版本中，加载数据最大值不能超过所有 query node 内存总量的 70%，从而为执行引擎预留内存资源。
</div>

3. 创建随机向量作为 `query_records` 并调用 `search()` 进行搜索。
*Milvus 将返回搜索结果的 ID 和距离：*


{{fragments/multiple_code.md}}

```python
>>> results = collection.search(vectors[:5], field_name, param=search_params, limit=10, expr=None)
>>> results[0].ids
[424363819726212428, 424363819726212436, ...]
>>> results[0].distances
[0.0, 1.0862197875976562, 1.1029295921325684, ...]
```

```javascript
await milvusClient.dataManager.search({
  collection_name: COLLECTION_NAME,
  // partition_names: [],
  expr: "",
  vectors: [[1, 2, 3, 4, 5, 6, 7, 8]],
  search_params: searchParams,
  vector_type: 100, // Float vector -> 100
});
```

如果要在指定分区或者指定列查询，则可以在调用 `search()` 时设置`partition_names` 和 `fields` 参数

{{fragments/multiple_code.md}}

```python
>>> collection.search(vectors[:5], field_name, param=search_params, limit=10, expr=None, partition_names=[partition_name])
```

```javascript
await milvusClient.dataManager.search({
  collection_name: COLLECTION_NAME,
  partition_names: [partition_name],
  expr: "",
  vectors: [[1, 2, 3, 4, 5, 6, 7, 8]],
  search_params: searchParams,
  vector_type: 100, // Float vector -> 100
});
```

4. 查询完成后，可以调用 `release_collection()` 将 Milvus 中加载的 collection 从内存中释放，以减少内存消耗。查询其他 collection：

{{fragments/multiple_code.md}}

```python
>>> collection.release()
```

```javascript
await milvusClient.collectionManager.releaseCollection({
  collection_name: COLLECTION_NAME,
});
```
