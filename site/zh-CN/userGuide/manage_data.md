---
id: manage_index.md
related_key: create index
summary: Learn how to build an index for vectors in Milvus.

---

# Manage Indexes

This topic describes how to manage indexes in Milvus. See [Vector Index](index.md) and [Index Selection](index_selection.md) for more information.

<div class="alert note">
Current release of Milvus only supports building and dropping index on vector field. Future releases will support these operations on scalar field.
</div>

## Build an index

Prepare the index parameters.

<div class="alert note">
By default, Milvus does not index a segment with less than 1,024 rows. To change this parameter, configure <a href="configuration_standalone-advanced.md#System-Behavior-Configurations"><code>minSegmentSizeToEnableIndex</code></a> in <code>root_coord.yaml</code>.
</div>


{{fragments/multiple_code.md}}

```python
>>> index_params = {
        "metric_type":"L2",
        "index_type":"IVF_FLAT",
        "params":{"nlist":1024}
    }
```

```javascript
const index_params = {
  metric_type: "L2",
  index_type: "IVF_FLAT",
  params: JSON.stringify({ nlist: 1024 }),
};
```

<table class="params">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>metric_type</code></td>
		<td>Metrics used to measure similarity of vectors. Find more options in <a href="metric.md">Simlarity Metrics</a>.</td>
	</tr>
	<tr>
		<td><code>index_type</code></td>
		<td>Type of index used to accelerate the vector search. Find more options in <a href="index_selection.md">Index Selection</a>.</td>
	</tr>
	<tr>
		<td><code>params</code></td>
		<td>Building parameter(s) specific to the index. See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	</tbody>
</table>


Build the index by specifying the vector field name and index parameters.

{{fragments/multiple_code.md}}

```python
>>> from pymilvus import collection
>>> collection = Collection("example_collection")      # Get an existing collection.
>>> collection.create_index(field_name="example_field", index_params=index_params)
```

```javascript
await milvusClient.indexManager.createIndex({
  collection_name: "example_collection",
  field_name: "example_field",
  extra_params: index_params,
});
```

```
Status(code=0, message='')
```



## View index details

{{fragments/multiple_code.md}}

```python
>>> from pymilvus import collection
>>> collection = Collection("example_collection")      # Get an existing collection.
>>> collection.index().params
```

```javascript
await milvusClient.indexManager.describeIndex({
  collection_name: "example_collection",
});
```

```
{'metric_type': 'L2', 'index_type': 'IVF_FLAT', 'params': {'nlist': 1024}}
```



## Drop an index

Drop the index of a specified field in a specified collection.

<div class="alert caution">
The drop operation is irreversible. Dropping an index removes all corresponding index files.
</div>



{{fragments/multiple_code.md}}

```python
>>> from pymilvus import collection>>> collection = Collection("example_collection")      # Get an existing collection.>>> collection.drop_index()
```

```javascript
await milvusClient.indexManager.dropIndex({  collection_name: "example_collection",});
```

## What's next

- Learn more basic operations of Milvus:
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)
  - [Search with Time Travel](timetravel.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

