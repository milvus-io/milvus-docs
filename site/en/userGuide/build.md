---
id: build.md
title: Build an Index for
---

# Build an Index

This page will show you how to create an index for a specified field in a collection to accelerate vector similarity search. See [Vector Index](index.md) for more information about setting index parameters.

1. Prepare the index parameters:

{{fragments/multiple_code.md}}

```python
>>> index_param = {
        "metric_type":"L2",
        "index_type":"IVF_FLAT",
        "params":{"nlist":1024}
    }
```

```javascript
const index_param = {
  metric_type: "L2",
  index_type: "IVF_FLAT",
  params: JSON.stringify({ nlist: 1024 }),
};
```

2. Build an index:

{{fragments/multiple_code.md}}

```python
>>> collection.create_index(field_name=field_name, index_params=index_param)
Status(code=0, message='')
```

```javascript
await milvusClient.indexManager.createIndex({
  collection_name: COLLECTION_NAME,
  field_name: FIELD_NAME,
  extra_params: index_param,
});
```

3. View index details:

{{fragments/multiple_code.md}}

```python
>>> collection.index().params
{'metric_type': 'L2', 'index_type': 'IVF_FLAT', 'params': {'nlist': 1024}}
```

```javascript
await milvusClient.indexManager.describeIndex({
  collection_name: COLLECTION_NAME,
});
```
