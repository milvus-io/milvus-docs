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
    		FieldSchema("example_field", dtype=DataType.FLOAT_VECTOR, dim=2)
		])
>>> collection = Collection("test_retrieve", schema, using='default', shards_num=2)
>>> import random
>>> data = [
    		[i for i in range(2000)],
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

```javascript
import { MilvusClient } from "@zilliz/milvus2-sdk-node";
const milvusClient = new MilvusClient("localhost:19530");
const params = {
  collection_name: "test_retrieve",
  fields: [
    {
      name: "example_field",
      description: "",
      data_type: DataType.FloatVector,
      type_params: {
        dim: "2",
      },
    },
    {
      name: "pk",
      data_type: DataType.Int64,
      is_primary_key: true,
      description: "",
    },
  ],
};
await milvusClient.collectionManager.createCollection(params);
const entities = Array.from({ length: 2000 }, (v,k) => ({
  "example_field": Array.from({ length: 2 }, () => Math.random()),
  "pk": k,
}));
await milvusClient.dataManager.insert({{
  collection_name: "test_retrieve",
  fields_data: entities,
});
const index_params = {
  metric_type: "L2",
  index_type: "IVF_FLAT",
  params: JSON.stringify({ nlist: 1024 }),
};
await milvusClient.indexManager.createIndex({
  collection_name: "test_retrieve",
  field_name: "example_field",
  extra_params: index_params,
});
```

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


<div class="alert warning">
In current release, volume of the data to load must be under 70% of the total memory resources of all query nodes to reserve memory resources for execution engine.
</div>

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

<table class="language-python">
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
		<td><code>params</code></td>
		<td>Search parameter(s) specific to the index. See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	</tbody>
</table>

<table class="language-javascript">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
	</tr>
	</thead>
	<tbody>
    <tr>
		<td><code>anns_field</code></td>
		<td>Name of the field to search on.</td>
	</tr>
	<tr>
		<td><code>topk</code></td>
		<td>Number of the most similar results to return.</td>
	</tr>
	<tr>
		<td><code>metric_type</code></td>
		<td>Metrics used to measure similarity of vectors. See <a href="metric.md">Simlarity Metrics</a> for more information.</td>
	</tr>
    <tr>
		<td><code>params</code></td>
		<td>Search parameter(s) specific to the index. See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	</tbody>
</table>


## Conduct a vector search

Search vectors with Milvus.

{{fragments/multiple_code.md}}

```python
>>> results = collection.search(data=[[0.1, 0.2]], anns_field="example_field", param=search_params, limit=10, expr=None)
```

```javascript
const results = await milvusClient.dataManager.search({
  collection_name: "test_retrieve",
  expr: "",
  vectors: [[0.1, 0.2]],
  search_params: searchParams,
  vector_type: 100, // Float vector -> 100
});
```

<table class="language-python">
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

<table class="language-javascript">
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
    <td>Parameters (as an object) used for search.</td>
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
>>> collection.search(data=[[0.1, 0.2]], "example_field", param=search_params, limit=10, expr=None, partition_names=["example_partition"])
```

```javascript
await milvusClient.dataManager.search({
  collection_name: "example_collection",
  partition_names: ["example_partition"],
  expr: "",
  vectors: [[0.1, 0.2]],
  search_params: searchParams,
  vector_type: 100, // Float vector -> 100
});
```

Check the primary key values of the most similar vectors and their distances.

{{fragments/multiple_code.md}}

```python
>>> results[0].ids
>>> results[0].distances
```

```javascript
console.log(results.results)
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
  - [Search with Time Travel](timetravel.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)