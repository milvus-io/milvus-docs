---
id: drop_index.md
related_key: drop index
summary: Learn how to drop an index in Milvus.
---

# Drop an Index

This topic describes how to drop an index in Milvus. 

<div class="alert caution">
Dropping an index irreversibly removes all corresponding index files.
</div>

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.
collection.drop_index()
```

```javascript
await milvusClient.indexManager.dropIndex({
  collection_name: "book",
});
```

```go
err := milvusClient.DropIndex(
    context.Background(),   // ctx
    "book",                 // CollectionName
    "book_intro",           // fieldName
    )
    if err != nil {
		// Handle error here.
	}
```

```java
milvusClient.dropIndex(
        DropIndexParam.newBuilder()
                .withCollectionName("book")
                .withFieldName("book_intro")
                .build());
```

```cli
delete index -c book
```


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
            <td>Name of the collection to drop index from.</td>
        </tr>
	</tbody>
</table>

<table class="language-go">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>ctx</code></td>
            <td>Context to control API invocation process.</td>
        </tr>
        <tr>
            <td><code>CollectionName</code></td>
            <td>Name of the collection to drop index on.</td>
        </tr>
        <tr>
            <td><code>fieldName</code></td>
            <td>Name of the vector field to drop index on.</td>
        </tr>
    </tbody>
</table>

<table class="language-java">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>CollectionName</code></td>
            <td>Name of the collection to drop index on.</td>
        </tr>
        <tr>
            <td><code>FieldName</code></td>
            <td>Name of the vector field to drop index on.</td>
        </tr>
    </tbody>
</table>

<table class="language-cli">
    <thead>
        <tr>
            <th>Option</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>-c</td>
            <td>Name of the collection to drop index from.</td>
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

