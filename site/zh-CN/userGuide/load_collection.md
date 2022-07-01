---
id: load_collection.md
related_key: load collection
summary: Learn how to load a collection into memory for CRUD operations in Milvus.
---

# 加载 Collection


{{fragments/translation_needed.md}}

当前主题介绍如何在搜索或查询之前将 collection 加载到内存中。 Milvus 中所有的搜索和查询操作都在内存中执行。

Milvus 2.1 allows users to load a collection as multiple replicas to utilize the CPU and memory resources of extra query nodes. This feature boost the overall QPS and throughput with extra hardware. It is supported on PyMilvus in current release.

<div class="alert warning">
<ul>
<li>在当前版本中，要加载的数据量必须低于所有 query node 总内存资源的 90%，以便为执行引擎预留内存资源。</li>
<li>In current release, all on-line query nodes will be divided into multiple replica groups according to the replica number specified by user. All replica groups shall have minimal memory resources to load one replica of the provided collection. Otherwise, an error will be returned.</li>
</ul>
</div>

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.
collection.load(replica_number=2)
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

<table class="language-python">
	<thead>
	<tr>
		<th>参数</th>
		<th>描述</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>partition_name</code> (optional)</td>
		<td>要加载的 partition 名称。</td>
	</tr>
    <tr>
		<td><code>replica_number</code> (optional)</td>
		<td>Number of the replica to load.</td>
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
		<td>要加载的 collection 名称。</td>
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
            <td>控制调用 API 的 Context。</td>
        </tr>
        <tr>
            <td><code>CollectionName</code></td>
            <td>要加载的 collection 名称。</td>
        </tr>
        <tr>
            <td><code>async</code></td>
            <td>Switch to control sync/async behavior. The deadline of context is not applied in sync load.切换以控制 sync/async 行为。Sync 加载中未应用 context 的截止日期。</td>
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
            <td>要加载的 collection 名称。</td>
        </tr>
    </tbody>
</table>

<table class="language-shell">
    <thead>
        <tr>
            <th>选项</th>
            <th>描述</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>-c</td>
            <td>要加载的 collection 名称。</td>
        </tr>
        <tr>
            <td>-p (Optional/Multiple)</td>
            <td>要加载的 partition 名称。</td>
        </tr>
    </tbody>
</table>


## Get replica information

You can check the information of the loaded replicas.

```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.
collection.load(replica_number=2)    # Load collection as 2 replicas
result = collection.get_replicas()
print(result)
```

## Constraints

- Error will be returned at the attempt to load partition(s) when the parent collection is already loaded. Future releases will support releasing partitions from a loaded collection, and (if needed) then loading some other partition(s).
- "Load successfully" will be returned at the attempt to load the collection that is already loaded.
- Error will be returned at the attempt to load the collection when the child partition(s) is/are already loaded. Future releases will support loading the collection when some of its partitions are already loaded.
- Loading different partitions in a same collection via separate RPCs is not allowed.

## 更多内容

- 了解更多 Milvus 的基本操作：
  - [插入数据](insert_data.md)
  - [创建 partition](create_partition.md)
  - [创建索引](build_index.md)
  - [进行向量搜索](search.md)
  - [进行混合搜索](hybridsearch.md)
- 探索 Milvus SDK 的 API 参考：
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

