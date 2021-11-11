---
id: query.md
related_key: query vectors
summary: Learn how to query vectors in Milvus.
---

# Conduct a Vector Query

This topic describes how to conduct a vector query.

Unlike a vector similarity search, a vector query retrieves vectors via scalar filtering based on [boolean expression](boolean.md). Milvus supports many data types in the scalar fields and a variety of boolean expressions. The boolean expression filters on scalar fields or the primary key field, and it retrieves all results that match the filters.

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

All CRUD operations within Milvus are executed in memory. Load the collection to memory before conducting a vector query.

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

## Conduct a vector query

The following example filters the vectors with certain `pk` values, and returns the `pk` field and `example_field` of the results.

{{fragments/multiple_code.md}}

```python
>>> res = collection.query(expr = "pk in [2,4,6,8]", output_fields = ["pk", "example_field"])
```

```javascript
await milvusClient.dataManager.query({
  collection_name: "test_retrieve",
  expr: "pk in [2,4,6,8]",
  output_fields: ["pk", "example_field"],
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
		<td><code>expr</code></td>
		<td>Boolean expression used to filter attribute. Find more expression details in <a href="boolean.md">Boolean Expression Rules</a>.</td>
	</tr>
	<tr>
		<td><code>output_fields</code> (optional)</td>
		<td>List of names of the field to return.</td>
	</tr>
	<tr>
		<td><code>partition_names</code> (optional)</td>
		<td>List of names of the partitions to query on.</td>
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
		<td>Name of the collection to query.</td>
	</tr>
	<tr>
		<td><code>expr</code></td>
		<td>Boolean expression used to filter attribute. Find more expression details in <a href="boolean.md">Boolean Expression Rules</a>.</td>
	</tr>
	<tr>
		<td><code>output_fields</code> (optional)</td>
		<td>List of names of the field to return.</td>
	</tr>
	<tr>
		<td><code>partition_names</code> (optional)</td>
		<td>List of names of the partitions to query on.</td>
	</tr>
	</tbody>
</table>


## What's next

- Learn more basic operations of Milvus:
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)
  - [Search with Time Travel](timetravel.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)
