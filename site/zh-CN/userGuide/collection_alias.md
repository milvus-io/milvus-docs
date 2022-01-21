---
id: collection_alias.md
related_key: collection alias
summary: Learn how to manage collection alias in Milvus.
---

# 集合别名

{{fragments/translation_needed.md}}

Milvus支持为集合指定唯一别名。

<div class="alert note">
集合别名是全局唯一，因此您不能给两个不同集合安排相同别名。但您可给一个集合安排几个别名。
</div>

下面的例子基于别名`publication`。


## 创建集合别名

为集合指定别名。

{{fragments/multiple_code.md}}

```python
from pymilvus import utility
utility.create_alias(
collection_name = "book",
alias = "publication"
)
```

```javascript
await milvusClient.collectionManager.createAlias({
  collection_name: "book",
  alias: "publication",
});
```

```cli
create alias -c book -a publication
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
            <td>要创建别名的集合名称。</td>
        </tr>
        <tr>
            <td><code>alias</code></td>
            <td>集合别名。</td>
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



## 删除集合别名

删除一个指定的别名。

{{fragments/multiple_code.md}}

```python
from pymilvus import utility
utility.drop_alias(
alias = "publication"
)
```

```javascript
await milvusClient.collectionManager.dropAlias({
  alias: "publication",
});
```

```cli
delete alias -c book -a publication
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


## 修改集合别名

修改一个存在的别名到另一个。

{{fragments/multiple_code.md}}

```python
from pymilvus import utility
utility.alter_alias(
collection_name = "book",
alias = "publication"
)
```

```javascript
await milvusClient.collectionManager.alterAlias({
  collection_name: "book",
  alias: "publication",
});
```

```cli
create alias -c book -A -a publication
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

## Limits

|Feature|Maximum limit|
|---|---|
|Length of an alias|255 characters|

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

