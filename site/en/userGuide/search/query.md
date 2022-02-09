---
id: query.md
related_key: query vectors
summary: Learn how to query vectors in Milvus.
---

# Conduct a Vector Query

This topic describes how to conduct a vector query.

Unlike a vector similarity search, a vector query retrieves vectors via scalar filtering based on [boolean expression](boolean.md). Milvus supports many data types in the scalar fields and a variety of boolean expressions. The boolean expression filters on scalar fields or the primary key field, and it retrieves all results that match the filters.

The following example shows how to perform a vector query on a 2000-row dataset of book ID (primary key), word count (scalar field), and book introduction (vector field), simulating the situation where you query for certain books based on their IDs.


## Load collection

All search and query operations within Milvus are executed in memory. Load the collection to memory before conducting a vector query.

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

```go
err := milvusClient.LoadCollection(
    context.Background(),   // ctx
    "book",                 // CollectionName
    false                   // async
    )
if err != nil {
    log.Fatal("failed to load collection:", err.Error())
}
```

```java
milvusClient.loadCollection(
        LoadCollectionParam.newBuilder()
                .withCollectionName("book")
                .build());
```

```shell
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
queryResult, err := milvusClient.Query(
	context.Background(),                                   // ctx
	"book",                                                 // CollectionName
	"",                                                     // PartitionName
	entity.NewColumnInt64("book_id", []int64{2,4,6,8}),     // expr
	[]string{"book_id", "book_intro"}                       // OutputFields
)
if err != nil {
	log.Fatal("fail to query collection:", err.Error())
}
```

```java
List<String> query_output_fields = Arrays.asList("book_id", "word_count");
QueryParam queryParam = QueryParam.newBuilder()
        .withCollectionName("book")
        .withExpr("book_id in [2,4,6,8]")
        .withOutFields(query_output_fields)
        .build();
R<QueryResults> respQuery = milvusClient.query(queryParam);
```

```shell
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
    <td><code>partitionName</code></td>
    <td>List of names of the partitions to load. All partitions will be queried if it is left empty.</td>
    <td>N/A</td>
  </tr>
  <tr>
		<td><code>expr</code></td>
		<td>Boolean expression used to filter attribute.</td>
    <td>See <a href="boolean.md">Boolean Expression Rules</a> for more information.</td>
	</tr>
    <tr>
		<td><code>OutputFields</code></td>
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


<table class="language-shell">
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
fmt.Printf("%#v\n", queryResult)
for _, qr := range queryResult {
	fmt.Println(qr.IDs)
}
```

```java
QueryResultsWrapper wrapperQuery = new QueryResultsWrapper(respQuery.getData());
System.out.println(wrapperQuery.getFieldWrapper("book_id").getFieldData());
System.out.println(wrapperQuery.getFieldWrapper("word_count").getFieldData());
```

```shell
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
