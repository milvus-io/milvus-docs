---
id: delete.md
title: Delete
---

# Delete operations

The delete operations affect data already inserted into Milvus. Think twice before you delete.

> The function of deleting specified vectors by ID is currently unavailable.

## Drop an index

Drop the index of a specified field in a specified collection:

{{fragments/multiple_code.md}}

```python
>>> collection.drop_index()
```

```javascript
await milvusClient.indexManager.dropIndex({
  collection_name: COLLECTION_NAME,
});
```

## Drop a partition

Remove a partition and all vectors under it:

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

## Drop a collection

When you no longer need a collection, you can delete it.

{{fragments/multiple_code.md}}

```python
>>> collection.drop()
```

```javascript
await milvusClient.collectionManager.dropCollection({
  collection_name: COLLECTION_NAME,
});
```


## Delete entities

This feature is still under development and will be available when a stable version of Milvus 2.0 is released.