---
id: query.md
related_key: query vectors
summary: Learn how to query vectors in Milvus.
---

# Conduct a Vector Query

This topic describes how to conduct a vector query.

Unlike a vector similarity search, a vector query retrieves vectors via scalar filtering based on [boolean expression](boolean.md). Milvus supports many data types in the scalar fields and a variety of boolean expressions. The boolean expression filters on scalar fields or the primary key field, and it retrieves all results that match the filters.

The following example shows how to perform a vector query on a 2000-row dataset of book ID (primary key), word count (scalar field), and book introduction (vector field), simulating the situation where you query for certain books based on their IDs.

## Preparations

The following example code demonstrates the steps prior to a query.

If you work with your own dataset in an existing Milvus server, you can move forward to the next step.

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

2. Create a collection. See [Create a Collection](create_collection.md) for more instruction.

{{fragments/multiple_code.md}}

```python
schema = CollectionSchema([
    		FieldSchema("book_id", DataType.INT64, is_primary=True),
			  FieldSchema("word_count", DataType.INT64),
    		FieldSchema("book_intro", dtype=DataType.FLOAT_VECTOR, dim=2)
		])
collection = Collection("book", schema, using='default', shards_num=2)
```

```javascript
const params = {
  collection_name: "book",
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
create collection -c book -f book_intro:FLOAT_VECTOR:2 -f book_id:INT64 book_id -f word_count:INT64 word_count -p book_id
```

3. Insert data into the collection (Milvus CLI example uses a pre-built, remote CSV file containing similar data). See [Insert Data](insert_data.md) for more instruction.

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
const data = Array.from({ length: 2000 }, (v,k) => ({
  "book_intro": Array.from({ length: 2 }, () => Math.random()),
  "book_id": k,
  "word_count": k+10000,
}));
await milvusClient.dataManager.insert({
  collection_name: "book",
  fields_data: entities,
});
```

```cli
import -c book 'https://raw.githubusercontent.com/milvus-io/milvus_cli/main/examples/user_guide/search.csv'
```

4. Create an index for the vector field. See [Build Index](build_index.md) for more instruction.

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
  collection_name: "book",
  field_name: "book_intro",
  extra_params: index_params,
});
```

```cli
create index

Collection name (book): book

The name of the field to create an index for (book_intro): book_intro

Index type (FLAT, IVF_FLAT, IVF_SQ8, IVF_PQ, RNSG, HNSW, ANNOY): IVF_FLAT

Index metric type (L2, IP, HAMMING, TANIMOTO): L2

Index params nlist: 1024

Timeout []:
```


## Load collection

All CRUD operations within Milvus are executed in memory. Load the collection to memory before conducting a vector query.

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.
collection.load()
```

```javascript
await milvusClient.collectionManager.loadCollection({
  collection_name: "book",
});
```

```cli
load -c book
```

<div class="alert warning">
In current release, volume of the data to load must be under 70% of the total memory resources of all query nodes to reserve memory resources for execution engine.
</div>

## Conduct a vector query

The following example filters the vectors with certain `book_id` values, and returns the `book_id` field and `book_intro` of the results.

{{fragments/multiple_code.md}}

```python
res = collection.query(expr = "book_id in [2,4,6,8]", output_fields = ["book_id", "book_intro"])
```

```javascript
const results = await milvusClient.dataManager.query({
  collection_name: "book",
  expr: "book_id in [2,4,6,8]",
  output_fields: ["book_id", "book_intro"],
});
```

```go
searchResult, err := milvusClient.Search(
  context.Background(),     // ctx
  "book",                   // CollectionName
  []string{},               // partitionNames
  "word_count <= 11000",    // expr
  []string{"book_id"},      // outputFields
  queryVector,              // vectors
  "Vector",                 // vectorField
  entity.L2,                // metricType
  2,                        // topK
  sp                        // sp
  )
```

```java
List<String> fields = Arrays.asList(PK_FIELD, SCALAR_FIELD);
QueryParam queryParam = QueryParam.newBuilder()
                .withCollectionName("book")
                .withExpr("book_id in [2,4,6,8]")
                .withOutFields(fields)
                .build();
R<QueryResults> response = milvusClient.query(queryParam);
QueryResultsWrapper wrapper = new QueryResultsWrapper(response.getData());
```

```cli
query

collection_name: book

The query expression: book_id in [2,4,6,8]

Name of partitions that contain entities(split by "," if multiple) []:

A list of fields to return(split by "," if multiple) []: book_id, book_intro

timeout []:
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

<table class="language-go">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
    <th>Options</th>
	</tr>
	</thead>
	<tbody>
  <tr>
    <td><code>ctx</code></td>
    <td>Context to control API invocation process.</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td><code>CollectionName</code></td>
    <td>Name of the collection to query.</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td><code>partitionNames</code></td>
    <td>List of names of the partitions to load. All partitions will be queried if it is left empty.</td>
    <td>N/A</td>
  </tr>
  <tr>
		<td><code>expr</code></td>
		<td>Boolean expression used to filter attribute.</td>
    <td>See <a href="boolean.md">Boolean Expression Rules</a> for more information.</td>
	</tr>
  <tr>
		<td><code>output_fields</code></td>
		<td>Name of the field to return.</td>
    <td>Vector field is not supported in current release.</td>
	</tr>
	</tbody>
</table>

<table class="language-java">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
    <th>Options</th>
	</tr>
	</thead>
	<tbody>
	<tr>
    <td><code>CollectionName</code></td>
    <td>Name of the collection to load.</td>
    <td>N/A</td>
  </tr>
  <tr>
		<td><code>OutFields</code></td>
		<td>Name of the field to return.</td>
    <td>Vector field is not supported in current release.</td>
	</tr>
  <tr>
		<td><code>Expr</code></td>
		<td>Boolean expression used to filter attribute.</td>
    <td>See <a href="boolean.md">Boolean Expression Rules</a> for more information.</td>
	</tr>
	</tbody>
</table>


<table class="language-cli">
    <thead>
        <tr>
            <th>Option</th>
            <th>Full name</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>--help</td>
            <td>n/a</td>
            <td>Displays help for using the command.</td>
        </tr>
    </tbody>
</table>


Check the returned results. 

{{fragments/multiple_code.md}}

```python
sorted_res = sorted(res, key=lambda k: k['book_id'])
sorted_res
```

```javascript
console.log(results.data)
```

```go

```

```java
System.out.println(PK_FIELD + ":" + wrapper.getFieldWrapper(PK_FIELD).getFieldData().toString());
System.out.println(SCALAR_FIELD + ":" + wrapper.getFieldWrapper(SCALAR_FIELD).getFieldData().toString());
System.out.println("Query row count: " + wrapper.getFieldWrapper(PK_FIELD).getRowCount());
```

```cli
# Milvus CLI automatically returns the entities with the pre-defined output fields.
```

## What's next

- Learn more basic operations of Milvus:
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)
  - [Search with Time Travel](timetravel.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)
