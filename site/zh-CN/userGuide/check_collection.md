---
id: check_collection.md
related_key: collection
summary: Learn how to check collection information in Milvus.
---

# Check Collection Information

{{fragments/translation_needed.md}}

This topic describes how to check the information of the collection in Milvus.

## Check if a collection exists

Verify if a collection exists in Milvus.

{{fragments/multiple_code.md}}

```python
from pymilvus import utility
utility.has_collection("book")
```

```javascript
await milvusClient.collectionManager.hasCollection({
  collection_name: "book",
});
```

```cli
describe collection -c book
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
            <td><code>collection_name</code></td>
            <td>Name of the collection to check.</td>
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
            <td>Name of the collection to check.</td>
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
            <td>Name of the collection to check.</td>
        </tr>
    </tbody>
</table>

## Check collection details

Check the details of a collection.

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.

collection.schema                                  # Return the schema.CollectionSchema of the collection.
collection.description                             # Return the description of the collection.
collection.name                                    # Return the name of the collection.
collection.is_empty                                # Return the boolean value that indicates if the collection is empty.
collection.num_entities                            # Return the number of entities in the collection.
collection.primary_field                           # Return the schema.FieldSchema of the primary key field.
collection.partitions                              # Return the list[Partition] object.
collection.indexes                                 # Return the list[Index] object.
```

```javascript
await milvusClient.collectionManager.describeCollection({          // Return the name and schema of the collection.
  collection_name: "book",
});

await milvusClient.collectionManager.getCollectionStatistics({     // Return the statistics information of the collection.
  collection_name: "book",
});
```

```cli
describe collection -c book
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
            <td>Name of the collection to check.</td>
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
            <td>Name of the collection to check.</td>
        </tr>
    </tbody>
</table>


## List all collections

List all collections in this Milvus Instance.

{{fragments/multiple_code.md}}

```python
from pymilvus import utility
utility.list_collections()
```

```javascript
await milvusClient.collectionManager.showCollections();
```

```cli
list collections
```

## What's next

- Learn more basic operations of Milvus:
  - [Insert data into Milvus](insert_data.md)
  - [Create a partition](create_partition.md)
  - [Build an index for vectors](build_index.md)
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

