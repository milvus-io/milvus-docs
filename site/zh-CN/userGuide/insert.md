---
id: insert.md
title: 插入数据
---

# 在集合中插入数据
你可以通过以下步骤在指定 collection 的指定 partition 中插入数据。

1.随机生成待插入的数据:

{{fragments/multiple_code.md}}

```python
>>> import random
>>> vectors = [[random.random() for _ in range(8)] for _ in range(10)]
>>> entities = [vectors]
```

```javascript
const entities = Array.from({ length: 10 }, () => ({
  [FIELD_NAME]: Array.from({ length: 8 }, () => Math.floor(Math.random() * 10)),
}));
```

2. 调用以上函数将随机生成的数据插入新创建的 collection 中。Milvus 会为每条插入的数据自动生成 ID，类似于关系型数据库中的 AutoID。

*Milvus 将返回 `MutationResult`，其中包含插入数据对应的主键列 `primary_keys`。*

{{fragments/multiple_code.md}}

```python
>>> mr = collection.insert(entities)
<pymilvus_orm.search.MutationResult object at 0x7fcfe8255550>
>>> mr.primary_keys
[425790736918318406, 425790736918318407, 425790736918318408, ...]
```

```javascript
await milvusClient.dataManager.insert({{
  collection_name: COLLECTION_NAME,
  fields_data: entities,
});
```

3. 调用 insert() 函数时指定 `partitiont_name` 可以将向量插入到指定的 Partition 中：

{{fragments/multiple_code.md}}

```python
>>> collection.insert(data=entities, partition_name=partition_name)
```

```javascript
await milvusClient.dataManager.insert({{
  collection_name: COLLECTION_NAME,
  partition_name: partition_name
  fields_data: entities,
});
```

4. 插入的数据将存储在 Milvus 内存中。调用 `flush()` 函数将数据落盘：

{{fragments/multiple_code.md}}

```python
>>> pymilvus_orm.utility.get_connection().flush([collection_name])
```

```javascript
await milvusClient.dataManager.flush({ collection_names: [COLLECTION_NAME] });
```