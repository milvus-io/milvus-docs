---
id: compact_data.md
related_key: compact data
summary: Learn how to compact data in Milvus.
---

# Compact Data

This topic describes how to compact data in Milvus.

Milvus supports automatic data compaction by default. You can [configure](configure-docker.md) your Milvus to enable or disable [compaction](configure_datacoord.md#dataCoordenableCompaction) and [automatic compaction](configure_datacoord.md#dataCoordcompactionenableAutoCompaction).

If automatic compaction is disabled, you can still compact data manually.

<div class="alert note">
To ensure accuracy of searches with Time Travel, Milvus retains the data operation log within the span specified in <a href="configure_common.md#common.retentionDuration"><code>common.retentionDuration</code></a>. Therefore, data operated within this period will not be compacted. 
</div>

## Compact data manually

Compaction requests are processed asynchronously because they are usually time-consuming. 

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.
collection.compact()
```

```javascript
const res = await milvusClient.collectionManager.compact({
  collection_name: "book",
});
const compactionID = res.compactionID;
```

```go
// This function is under active development on the GO client.
```

```java
R<ManualCompactionResponse> response = milvusClient.manualCompaction(
  ManualCompactionParam.newBuilder()
    .withCollectionName("book")
    .build()
);
long compactionID = response.getData().getCompactionID();
```

```shell
compact -c book
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
		<td>Name of the collection to compact data.</td>
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
            <td>Name of the collection to compact data.</td>
        </tr>
    </tbody>
</table>

<table class="language-shell">
    <thead>
        <tr>
            <th>Option</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>-c</td>
            <td>Name of the collection to compact data.</td>
        </tr>
    </tbody>
</table>

## Check compaction status

You can check the compaction status with the compaction ID returned when the manual compaction is triggered.

{{fragments/multiple_code.md}}

```python
collection.get_compaction_state()
```

```javascript
const state = await milvusClient.collectionManager.getCompactionState({
    compactionID
});
```

```go
// This function is under active development on the GO client.
```

```java
milvusClient.getCompactionState(GetCompactionStateParam.newBuilder()
  .withCompactionID(compactionID)
  .build()
);
```

```shell
show compaction_state -c book
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

