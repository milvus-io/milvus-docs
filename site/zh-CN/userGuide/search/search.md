---
id: search.md
related_key: search
summary: Conduct a vector similarity search with Milvus.
---

# Conduct a Vector Similarity Search

This topic describes how to search entities with Milvus.

## Preparations

Connect to Milvus server, create a collection, insert data, and build index for the entities.

If you work with your own dataset in an existing Milvus server, you can move forward to the next step.

```python
>>> from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
>>> connections.connect("default", host='localhost', port='19530')
>>> schema = CollectionSchema([
    		FieldSchema("pk", DataType.INT64, is_primary=True),
    		FieldSchema("example_field", dtype=DataType.FLOAT_VECTOR, dim=8)
		])
>>> collection = Collection("test_retrieve", schema, using='default', shards_num=2)
>>> import random
>>> data = [
    		[i for i in range(10)],
    		[[random.random() for _ in range(2)] for _ in range(2000)],
		]
>>> collection.insert(data)
>>> index_params = {
        "metric_type":"L2",
        "index_type":"IVF_FLAT",
        "params":{"nlist":1024}
    }
>>> collection.create_index("example_field", index_params=index_param)
```

## Prepare search parameters

{{fragments/multiple_code.md}}

```python
>>> search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
```

```javascript
const searchParams = {
  anns_field: "example_field",
  topk: "10",
  metric_type: "L2",
  params: JSON.stringify({ nprobe: 10 }),
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
		<td>Metrics used to measure similarity of vectors. See <a href="metric.md">Simlarity Metrics</a> for more information.</td>
	</tr>
	<tr>
		<td><code>index_type</code></td>
		<td>Type of index used to accelerate the vector search. See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
    <tr>
		<td><code>params</code></td>
		<td>Search parameter(s) specific to the index. See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	</tbody>
</table>

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
		<td>Metrics used to measure similarity of vectors. See <a href="metric.md">Simlarity Metrics</a> for more information.</td>
	</tr>
	<tr>
		<td><code>index_type</code></td>
		<td>Type of index used to accelerate the vector search. See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
    <tr>
		<td><code>params</code></td>
		<td>Search parameter(s) specific to the index. See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
    <tr>
		<td><code>anns_field</code></td>
		<td>Name of the field to search on.</td>
	</tr>
	<tr>
		<td><code>topk</code></td>
		<td>Number of the most similar results to return.</td>
	</tr>
	</tbody>
</table>

## Load collection

All CRUD operations within Milvus are executed in memory. Load the collection to memory before conducting a vector similarity search.

{{fragments/multiple_code.md}}

```python
>>> from pymilvus import collection
>>> collection = Collection("test_retrieve")      # Get an existing collection.
>>> collection.load()
```

```javascript
await milvusClient.collectionManager.loadCollection({
  collection_name: "test_retrieve",
});
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
		<td><code>partition_name</code> (optional)</td>
		<td>Name of the partition to load.</td>
	</tr>
	</tbody>
</table>

<table class="params">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>collection_name</code></td>
		<td>Name of the collection to load.</td>
	</tr>
	</tbody>
</table>

<div class="alert warning">
In current release, volume of the data to load must be under 70% of the total memory resources of all query nodes to reserve memory resources for execution engine.
</div>

## Conduct a vector search

Milvus returns the IDs of the most similar vectors and their distances.

{{fragments/multiple_code.md}}

```python
>>> results = collection.search(data=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]], anns_field="example_field", param=search_params, limit=10, expr=None)
>>> results[0].ids
[424363819726212428, 424363819726212436, ...]
>>> results[0].distances
[0.0, 1.0862197875976562, 1.1029295921325684, ...]
```

```javascript
await milvusClient.dataManager.search({
  collection_name: "test_retrieve",
  expr: "",
  vectors: [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]],
  search_params: searchParams,
  vector_type: 100, // Float vector -> 100
});
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
		<td><code>data</code></td>
		<td>Vectors to search with.</td>
	</tr>
	<tr>
		<td><code>anns_field</code></td>
		<td>Name of the field to search on.</td>
	</tr>
  <tr>
		<td><code>params</code></td>
		<td>Search parameter(s) specific to the index. See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	<tr>
		<td><code>limit</code></td>
		<td>Number of the most similar results to return.</td>
	</tr>
  <tr>
		<td><code>expr</code></td>
		<td>Boolean expression used to filter attribute. See <a href="boolean.md">Boolean Expression Rules</a> for more information.</td>
	</tr>
  <tr>
		<td><code>partition_names</code> (optional)</td>
		<td>List of names of the partition to search in.</td>
	</tr>
  <tr>
		<td><code>output_fields</code> (optional)</td>
		<td>Name of the field to return (vector field is not support in current release).</td>
	</tr>
  <tr>
		<td><code>timeout</code></td>
		<td>A duration of time in seconds to allow for RPC. Clients wait until server responds or error occurs when it is set to None.</td>
	</tr>
  <tr>
		<td><code>round_decimal</code></td>
		<td>Number of decimal places of returned distance.</td>
	</tr>
	</tbody>
</table>

<table class="params">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>collection_name</code></td>
		<td>Name of the collection to search in.</td>
	</tr>
	<tr>
    <td><code>search_params</code></td>
    <td>Parameters used for search.</td>
  </tr>
	<tr>
    <td><code>vectors</code></td>
    <td>Vectors to search with.</td>
  </tr>
  <tr>
		<td><code>vector_type</code></td>
		<td>Pre-check of binary or float vectors. <code>100</code> for binary vectors and <code>101</code> for float vectors.</td>
	</tr>
  <tr>
		<td><code>partition_names</code> (optional)</td>
		<td>List of names of the partition to search in.</td>
	</tr>
    <tr>
		<td><code>expr</code> (optional)</td>
		<td>Boolean expression used to filter attribute. See <a href="boolean.md">Boolean Expression Rules</a> for more information.</td>
	</tr>
  <tr>
		<td><code>output_fields</code> (optional)</td>
		<td>Name of the field to return (vector field not support in current release)</td>
	</tr>
	</tbody>
</table>

To search in a specific partition or field, specify the list of partition names and field name.

{{fragments/multiple_code.md}}

```python
>>> collection.search(data=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]], "example_field", param=search_params, limit=10, expr=None, partition_names=["example_partition"])
```

```javascript
await milvusClient.dataManager.search({
  collection_name: "example_collection",
  partition_names: ["example_partition"],
  expr: "",
  vectors: [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]],
  search_params: searchParams,
  vector_type: 100, // Float vector -> 100
});
```

Release the collection loaded in Milvus to reduce memory consumption when the search is completed.

{{fragments/multiple_code.md}}

```python
>>> collection.release()
```

```javascript
await milvusClient.collectionManager.releaseCollection({  collection_name: "test_retrieve",});
```

## What's next

- Learn more basic operations of Milvus:
  - [Query vectors](query.md)
  - [Conduct a hybrid search](hybridsearch.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)