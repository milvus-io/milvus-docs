---
id: build.md
related_key: create index
summary: Learn how to build an index for vectors in Milvus.

---

# Build an Index

This topic describes how to build an index for a field. See [Vector Index](index.md) for more information about setting index parameters.

<div class="alert note">
Parameters marked with `*` are specific to Python SDK, and those marked with `**` are specific to Node.js SDK.
</div>

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

<details>
  <summary><b>Detailed Description</b></summary>
<table class="params">
	<thead>
	<tr>
		<th>Parameter</td>
		<th>Description</th>
		<th>Note</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td>metric_type</td>
		<td>Metrics used to measure similarity of vectors</td>
		<td>Find more options in <a href="metric.md">Simlarity Metrics</a>.<br/>Mandatory</td>
	</tr>
	<tr>
		<td>index_type</td>
		<td>Type of index used to accelerate the vector search</td>
		<td>Find more options in <a href="index_selection.md">Index Selection</a>.<br/>Mandatory</td>
	</tr>
	<tr>
		<td>params</td>
		<td>Building parameter(s) specific to the index</td>
		<td>Find more parameter details of different indexes in <a href="index_selection.md">Index Selection</a>.<br/>Mandatory</td>
	</tr>
	</tbody>
</table>
</details>

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
