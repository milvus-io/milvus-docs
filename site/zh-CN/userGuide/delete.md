---
id: delete.md
---
# 删除操作
删除操作会影响已经插入 Milvus 系统的数据，请谨慎操作。

> 通过ID删除指定向量的功能还未开放。

## 删除索引
调用 `drop_index()` 函数删除指定 collection 指定列的索引：


{{fragments/multiple_code.md}}


```python
>>> collection.drop_index()
```

```javascript
await milvusClient.indexManager.dropIndex({
  collection_name: COLLECTION_NAME,
});
```

## 删除 partition
调用 `drop_partition()` 删除指定 partition 及其中的数据：


{{fragments/multiple_code.md}}


```python
>>> collection.drop_partition(partition_name=partition_name)
```

```javascript
await milvusClient.partitionManager.dropPartition({
  collection_name: COLLECTION_NAME,
  partition_name: PARTITION_NAME,
});
```


## 删除 collection
调用 `drop_collection()` 删除指定 collection：


{{fragments/multiple_code.md}}


```python
>>> collection.drop()
```

```javascript
await milvusClient.collectionManager.dropCollection({
  collection_name: COLLECTION_NAME,
});
```
