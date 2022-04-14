---
id: create_partition.md
related_key: Partition
summary: Learn how to create a partition in Milvus.
---

# 创建 Partition

{{fragments/translation_needed.md}}

本章描述如何在 Milvus 中创建 Partition。

Milvus 允许将大量的向量数据划分成一定数量的 Partition ，可以将搜索和其他操作限制在特定的 Partition 上来提高性能。

一个 Collection 由一个或多个 Partition 构成。创建新 Collection 时, Milvus 会创建一个名为`_default`的默认 Partition 。 Partition 的详细介绍参见 [术语表 - Partition](glossary.md#Partition) 。

下面的示例代码会在 Collection `book`中创建 Partition `novel`。


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
		<td>待创建的 Partition 名称。</td>
	</tr>
  <tr>
		<td><code>description</code> (可选)</td>
		<td>待创建的 Partition 描述。</td>
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
      <td>待创建 Partition 的 Collection 名称。</td>
    </tr>
    <tr>
      <td><code>partition_name</code></td>
      <td>待创建的 Partition 名称。</td>
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
        <td>待创建 Partition 的 Collection 名称。</td>
    </tr>
    <tr>
        <td><code>partitionName</code></td>
        <td>待创建的 Partition 名称。</td>
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
        <td>待创建 Partition 的 Collection 名称。</td>
    </tr>
    <tr>
        <td><code>PartitionName</code></td>
        <td>待创建的 Partition 名称。</td>
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
            <td>Collection 名称</td>
        </tr>
        <tr>
            <td>-p</td>
            <td>Partition 名称</td>
        </tr>
        <tr>
            <td>-d (可选)</td>
            <td>Partition 描述</td>
        </tr>
    </tbody>
</table>

## 限制
|设置项 |最大数量限制|
|---|---|
|单个 Collection 中的 Partition 数量|4,096|

## 更多内容

- 学习 Milvus 更多基础操作：
  - [在 Milvus 中插入数据](insert_data.md)
  - [创建向量索引](build_index.md)
  - [向量检索](search.md)
  - [混合检索](hybridsearch.md)
- 探索 Milvus SDKs 中的 API：
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

