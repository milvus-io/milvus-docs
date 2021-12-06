---
id: hybridsearch.md
related_key: filter
summary: Conduct a Hybrid Search with Milvus.
---

# Conduct a Hybrid Search

This topic describes how to conduct a hybrid search.

A hybrid search is essentially a vector search with attribute filtering. By specifying [boolean expressions](boolean.md) that filter the scalar fields or the primary key field, you can limit your search with certain conditions.

The following example shows how to perform a hybrid search on the basis of a regular [vector search](search.md). Suppose you want to search for certain books based on their vectorized introductions, but you only want those within a specific range of word count. You can then specify the boolean expression to filter the `word_count` field in the search parameters. Milvus will search for similar vectors only among those entities that match the expression.

## Preparations

The following example code demonstrates the steps prior to a search.

If you work with your own dataset in an existing Milvus instance, you can move forward to the next step.

1.  Connect to the Milvus server. See [Manage Connection](manage_connection.md) for more instruction.

{{fragments/multiple_code.md}}

```python
from pymilvus import connections
connections.connect("default", host='localhost', port='19530')
```

```javascript
const { MilvusClient } =require("@zilliz/milvus2-sdk-node");
const milvusClient = new MilvusClient("localhost:19530");
```

```cli
connect -h localhost -p 19530 -a default
```

2. Create a collection. See [Manage Collection](manage_collection.md) for more instruction.

{{fragments/multiple_code.md}}

```python
schema = CollectionSchema([
    		FieldSchema("book_id", DataType.INT64, is_primary=True),
			FieldSchema("word_count", DataType.INT64),
    		FieldSchema("book_intro", dtype=DataType.FLOAT_VECTOR, dim=2)
		])
collection = Collection("test_book_search", schema, using='default', shards_num=2)
```

```javascript
const params = {
  collection_name: "test_book_search",
  fields: [
    {
      name: "book_intro",
      description: "",
      data_type: 101,  // DataType.FloatVector
      type_params: {
        dim: "2",
      },
    },
	{
      name: "book_id",
      data_type: 5,   //DataType.Int64
      is_primary_key: true,
      description: "",
    },
    {
      name: "word_count",
      data_type: 5,    //DataType.Int64
      description: "",
    },
  ],
};
await milvusClient.collectionManager.createCollection(params);
```

```cli
create collection -c test_book_search -f book_intro:FLOAT_VECTOR:2 -f book_id:INT64 book_id -f word_count:INT64 word_count -p book_id
```

3. Insert data into the collection (Milvus CLI example uses a pre-built, remote CSV file containing similar data). See [Manage Data](manage_data.md) for more instruction.

{{fragments/multiple_code.md}}

```python
import random
data = [
    		[i for i in range(2000)],
			[i for i in range(10000, 12000)],
    		[[random.random() for _ in range(2)] for _ in range(2000)],
		]
collection.insert(data)
```

```javascript
const entities = Array.from({ length: 2000 }, (v,k) => ({
  "book_intro": Array.from({ length: 2 }, () => Math.random()),
  "book_id": k,
  "word_count": k+10000,
}));
await milvusClient.dataManager.insert({
  collection_name: "test_book_search",
  fields_data: entities,
});
```

```cli
import -c test_book_search 'https://raw.githubusercontent.com/milvus-io/milvus_cli/main/examples/user_guide/search.csv'
```

4. Create an index for the vector field. See [Manage Index](manage_index.md) for more instruction.

{{fragments/multiple_code.md}}

```python
index_params = {
        "metric_type":"L2",
        "index_type":"IVF_FLAT",
        "params":{"nlist":1024}
    }
collection.create_index("book_intro", index_params=index_params)
```

```javascript
const index_params = {
  metric_type: "L2",
  index_type: "IVF_FLAT",
  params: JSON.stringify({ nlist: 1024 }),
};
await milvusClient.indexManager.createIndex({
  collection_name: "test_book_search",
  field_name: "book_intro",
  extra_params: index_params,
});
```

```cli
create index

Collection name (test_book_search): test_book_search

The name of the field to create an index for (book_intro): book_intro

Index type (FLAT, IVF_FLAT, IVF_SQ8, IVF_PQ, RNSG, HNSW, ANNOY): IVF_FLAT

Index metric type (L2, IP, HAMMING, TANIMOTO): L2

Index params nlist: 1024

Timeout []:
```


## Load collection

All CRUD operations within Milvus are executed in memory. Load the collection to memory before conducting a vector search.

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("test_book_search")      # Get an existing collection.
collection.load()
```

```javascript
await milvusClient.collectionManager.loadCollection({
  collection_name: "test_book_search",
});
```

```cli
load -c test_book_search
```


<div class="alert warning">
In current release, volume of the data to load must be under 70% of the total memory resources of all query nodes to reserve memory resources for execution engine.
</div>

## Conduct a hybrid vector search

By specifying the boolean expression, you can filter the scalar field of the entities during the vector search. The following example limits the scale of search to the vectors within a specified `word_count` value range.

{{fragments/multiple_code.md}}

```python
search_param = {
    "data": [[0.1, 0.2]],
    "anns_field": "book_intro",
    "param": {"metric_type": "L2", "params": {"nprobe": 10}},
    "limit": 2,
    "expr": "word_count <= 11000",
}
res = collection.search(**search_param)
```

```javascript
const results = await milvusClient.dataManager.search({
  collection_name: "test_book_search",
  expr: "word_count <= 11000",
  vectors: [[0.1, 0.2]],
  search_params: {
    anns_field: "book_intro",
    topk: "2",
    metric_type: "L2",
    params: JSON.stringify({ nprobe: 10 }),
  },
  vector_type: 101,    // DataType.FloatVector,
});
```

```cli
search

Collection name (test_book_search): test_book_search

The vectors of search data(the length of data is number of query (nq), the dim of every vector in data must be equal to vector field’s of collection. You can also import a csv file without headers): [[0.1, 0.2]]

The vector field used to search of collection (book_intro): book_intro

Metric type: L2

Search parameter nprobe's value: 10

The max number of returned record, also known as topk: 2

The boolean expression used to filter attribute []: word_count <= 11000

The names of partitions to search (split by "," if multiple) ['_default'] []: 

timeout []:

Guarantee Timestamp(It instructs Milvus to see all operations performed before a provided timestamp. If no such timestamp is provided, then Milvus will search all operations performed to date) [0]: 

Travel Timestamp(Specify a timestamp in a search to get results based on a data view) [0]:
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
		<td>Name of the field to return. Vector field is not supported in current release.</td>
	</tr>
  <tr>
		<td><code>timeout</code> (optional)</td>
		<td>A duration of time in seconds to allow for RPC. Clients wait until server responds or error occurs when it is set to None.</td>
	</tr>
  <tr>
		<td><code>round_decimal</code> (optional)</td>
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
		<td>Name of the field to return. Vector field not support in current release.</td>
	</tr>
	</tbody>
</table>

Check the returned results:

{{fragments/multiple_code.md}}

```python
assert len(res) == 1
hits = res[0]
assert len(hits) == 2
print(f"- Total hits: {len(hits)}, hits ids: {hits.ids} ")
print(f"- Top1 hit id: {hits[0].id}, distance: {hits[0].distance}, score: {hits[0].score} ")
```

```javascript
console.log(results.results)
```

```cli
# Milvus CLI automatically returns the primary key values of the most similar vectors and their distances.
```
## What's next

- Learn more basic operations of Milvus:
  - [Search with Time Travel](timetravel.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)
