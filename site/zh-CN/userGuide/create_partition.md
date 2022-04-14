---
id: create_partition.md
related_key: Partition
summary: Learn how to create a partition in Milvus.
---

# 创建Partition

{{fragments/translation_needed.md}}

本章描述如何在Milvus中创建分区(Partition)。

Milvus允许将大量的矢量数据划分成一定数量的分区，可以将搜索和其他操作限制在特定的分区上来提高性能。

一个集合(Collection)由一个或多个分区构成。创建新集合时, Milvus会创建一个名为`_default`的默认分区。 分区的详细介绍参见 [术语表 - Partition](glossary.md#Partition) 。

下面的示例代码会在`book`集合中创建`novel`分区。


{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.
collection.create_partition("novel")
```

```javascript
await milvusClient.partitionManager.createPartition({
  collection_name: "book",
  partition_name: "novel",
});
```

```go
err := milvusClient.CreatePartition(
    context.Background(),   // ctx
    "book",                 // CollectionName
    "novel"                 // partitionName
)
if err != nil {
    log.Fatal("failed to create partition:", err.Error())
}
```

```java
milvusClient.createPartition(
        CreatePartitionParam.newBuilder()
                .withCollectionName("book")
                .withPartitionName("novel")
                .build());
```

```shell
create partition -c book -p novel
```


<table class="language-python">
	<thead>
	<tr>
		<th>参数</th>
		<th>描述</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>partition_name</code></td>
		<td>待创建的分区名称。</td>
	</tr>
  <tr>
		<td><code>description</code> (可选)</td>
		<td>待创建的分区描述。</td>
	</tr>
	</tbody>
</table>


<table class="language-javascript">
	<thead>
    <tr>
      <th>参数</th>
      <th>描述</th>
    </tr>
	</thead>
	<tbody>
    <tr>
      <td><code>collection_name</code></td>
      <td>待创建分区的集合名。</td>
    </tr>
    <tr>
      <td><code>partition_name</code></td>
      <td>待创建的分区名称。</td>
    </tr>
	</tbody>
</table>

<table class="language-go">
	<thead>
    <tr>
        <th>参数</th>
        <th>描述</th>
    </tr>
	</thead>
	<tbody>
    <tr>
        <td><code>ctx</code></td>
        <td>Context to control API invocation process.</td>
    </tr>
    <tr>
        <td><code>CollectionName</code></td>
        <td>待创建分区的集合名。</td>
    </tr>
    <tr>
        <td><code>partitionName</code></td>
        <td>待创建的分区名称。</td>
    </tr>
  </tbody>
</table>

<table class="language-java">
	<thead>
    <tr>
        <th>参数</th>
        <th>描述</th>
    </tr>
	</thead>
	<tbody>
    <tr>
        <td><code>CollectionName</code></td>
        <td>待创建分区的集合名。</td>
    </tr>
    <tr>
        <td><code>PartitionName</code></td>
        <td>待创建的分区名称。</td>
    </tr>
  </tbody>
</table>

<table class="language-shell">
    <thead>
        <tr>
            <th>参数</th>
            <th>描述</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>-c</td>
            <td>集合名称</td>
        </tr>
        <tr>
            <td>-p</td>
            <td>分区名称</td>
        </tr>
        <tr>
            <td>-d (可选)</td>
            <td>分区描述</td>
        </tr>
    </tbody>
</table>

## 限制
|设置项 |最大数量限制|
|---|---|
|单个集合中的分区数量|4,096|

## What's next

- Learn more basic operations of Milvus:
  - [Insert data into Milvus](insert_data.md)
  - [Build an index for vectors](build_index.md)
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

