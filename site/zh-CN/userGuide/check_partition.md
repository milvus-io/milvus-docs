---
id: check_partition.md
related_key: Partition
summary: Learn how to check partition information in Milvus.
---

# Check Partition Information

This topic describes how to check the information of the partition in Milvus.

## Verify if a partition exist

Verify if a partition exists in the specified collection.

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("example_collection")      # Get an existing collection.
collection.has_partition("example_partition")
```

```javascript
await milvusClient.partitionManager.hasPartition({
  collection_name: "example_collection",
  partition_name: "example_partition",
});
```

```cli
describe partition -c example_collection -p example_partition
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
            <td><code>partition_name</code></td>
            <td>Name of the partition to check.</td>
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
        <tr>
            <td><code>partition_name</code></td>
            <td>Name of the partition to check.</td>
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
        <tr>
            <td>-p</td>
            <td>Name of the partition to check.</td>
        </tr>
    </tbody>
</table>


## List all partitions

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("example_collection")      # Get an existing collection.
collection.partitions
```

```javascript
await milvusClient.partitionManager.showPartitions({
  collection_name: "example_collection",
});
```

```cli
list partitions -c example_collection
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


## What's next

- Learn more basic operations of Milvus:
  - [Insert data into Milvus](insert_data.md)
  - [Build an index for vectors](build_index.md)
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

