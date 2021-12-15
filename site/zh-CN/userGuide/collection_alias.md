---
id: collection_alias.md
related_key: collection alias
summary: Learn how to manage collection alias in Milvus.
---

# Collection Alias

Milvus supports specifying a unique alias for a collection.

<div class="alert note">
A collection alias is globally unique, hence you cannot assign the same alias to different collections. However, you can assign multiple aliases to one collection.
</div>


## Create a collection alias

Specify an an alias for a collection.

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("example_collection")      # Get an existing collection.
collection.create_alias("example_alias")
```

```javascript
await milvusClient.collectionManager.createAlias({
  collection_name: "example_collection",
  alias: "example_alias",
});
```

```cli
create alias -c example_collection -a example_alias
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
            <td>Name of the collection to create alias on.</td>
        </tr>
        <tr>
            <td><code>alias</code></td>
            <td>Collection alias to create.</td>
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
            <td>Name of the collection to create alias on.</td>
        </tr>
        <tr>
            <td><code>alias</code></td>
            <td>Collection alias to create.</td>
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
            <td>Name of the collection to create alias on.</td>
        </tr>
        <tr>
            <td>-a</td>
            <td>Collection alias to create.</td>
        </tr>
        <tr>
            <td>-A (Optional)</td>
            <td>Flag to transfer the alias to a specified collection.</td>
        </tr>
    </tbody>
</table>



## Drop a collection alias

Drop a specified alias.

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection.drop_alias("example_alias")
```

```javascript
await milvusClient.collectionManager.dropAlias({
  alias: "example_alias",
});
```

```cli
delete alias -c example_collection -a example_alias
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
            <td><code>alias</code></td>
            <td>Collection alias to drop.</td>
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
            <td><code>alias</code></td>
            <td>Collection alias to drop.</td>
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
            <td>Name of the collection to drop alias on.</td>
        </tr>
        <tr>
            <td>-a</td>
            <td>Collection alias to drop.</td>
        </tr>
    </tbody>
</table>


## Alter a collection alias

Alter an existing alias to another collection.

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("example_collection")      # Get an existing collection.
collection.alter_alias("example_alias")
```

```javascript
await milvusClient.collectionManager.alterAlias({
  collection_name: "example_collection",
  alias: "example_alias",
});
```

```cli
create alias -c example_collection -A -a example_alias
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
            <td>Name of the collection to alter alias to.</td>
        </tr>
        <tr>
            <td><code>alias</code></td>
            <td>Collection alias to alter.</td>
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
            <td>Name of the collection to alter alias to.</td>
        </tr>
        <tr>
            <td><code>alias</code></td>
            <td>Collection alias to alter.</td>
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
            <td>Name of the collection to alter alias to.</td>
        </tr>
        <tr>
            <td>-a</td>
            <td>Collection alias to alter.</td>
        </tr>
        <tr>
            <td>-A</td>
            <td>Flag to transfer the alias to a specified collection.</td>
        </tr>
    </tbody>
</table>

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

