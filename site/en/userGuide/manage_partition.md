---
id: manage_partition.md
related_key: Partition
summary: Learn how to manage partitions in Milvus.

---

# Manage Partitions

This topic describes how to manage partitions in Milvus.

Search performance drops as data volume increases in a collection. To mitigate the declining search performance, you can divide the bulk of data via partitioning. By dividing the data and storing them in separate partitions, you can narrow the range of a search to a partition and thereby improve the search performance.

A collection consists of one or more partitions. While creating a new collection, Milvus creates a default partition `_default`. See [Glossary - Partition](glossary.md#Partition) for more information.

This topic is based on a partition `example_partition` in the collection `example_collection`.

## Create a partition

{{fragments/multiple_code.md}}

```python
>>> from pymilvus import Collection
>>> collection = Collection("example_collection")      # Get an existing collection.
>>> partition = collection.create_partition("example_partition")
```

```javascript
await milvusClient.partitionManager.createPartition({
  collection_name: "example_collection",
  partition_name: "example_partition",
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
		<td><code>partition_name</code></td>
		<td>Name of the partition to create.</td>
	</tr>
  <tr>
		<td><code>description</code> (optional)</td>
		<td>Description of the partition to create.</td>
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
		<td>Name of the collection to create a partition in.</td>
	</tr>
  <tr>
		<td><code>partition_name</code></td>
		<td>Name of the partition to create.</td>
	</tr>
	</tbody>
</table>

## List all partitions

{{fragments/multiple_code.md}}

```python
>>> from pymilvus import Collection
>>> collection.partitions
```

```javascript
await milvusClient.partitionManager.showPartitions({
  collection_name: "example_collection",
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
		<td><code>collection_name</code></td>
		<td>Name of the collection to list partitions in.</td>
	</tr>
	</tbody>
</table>


## Verify if a partition exist

{{fragments/multiple_code.md}}

```python
>>> from pymilvus import Collection
>>> collection.has_partition("example_partition")
```

```javascript
await milvusClient.partitionManager.hasPartition({
  collection_name: "example_collection",
  partition_name: "example_partition",
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
		<td><code>partition_name</code></td>
		<td>Name of the partition to verify.</td>
	</tr>
  <tr>
		<td><code>timeout</code> (optional)</td>
		<td>A duration of time in seconds to allow for the RPC. When timeout is set to <code>None</code>, client waits until server responds or error occurs.</td>
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
		<td>Name of the collection to verify a partition in.</td>
	</tr>
  <tr>
		<td><code>partition_name</code></td>
		<td>Name of the partition to verify.</td>
	</tr>
	</tbody>
</table>


## Drop a partition

Remove a partition.

<div class="alert caution">
The drop operation is irreversible. Dropping a partition deletes all data within it.
</div>


{{fragments/multiple_code.md}}

```python
>>> from pymilvus import Collection
>>> collection.drop_partition("example_partition")
```

```javascript
await milvusClient.partitionManager.dropPartition({
  collection_name: "example_collection",
  partition_name: "example_partition",
});
```

<table class="params">
	<thead>
	<tr>
		<th>Parameter</td>
		<th>Description</th>
	</tr>
	</thead>
	<tbody>
 	<tr>
		<td><code>partition_name</code></td>
		<td>Name of the partition to drop.</td>
	</tr>
  <tr>
		<td><code>timeout</code> (optional)</td>
		<td>A duration of time in seconds to allow for the RPC. When timeout is set to <code>None</code>, client waits until server responds or error occurs.</td>
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
		<td><code>partition_name</code></td>
		<td>Name of the partition to drop.</td>
	</tr>
	<tr>
		<td><code>collection_name</code></td>
		<td>Name of the collection to drop partition from.</td>
	</tr>
	</tbody>
</table>


## What's next

- Learn more basic operations of Milvus:
  - [Insert data into Milvus](manage_data.md)
  - [Build an index for vectors](manage_index.md)
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

