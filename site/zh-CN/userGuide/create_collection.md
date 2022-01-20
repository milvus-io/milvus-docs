---
id: create_collection.md
related_key: create collection
summary: Learn how to create a collection in Milvus.
---

# 创建集合

{{fragments/translation_needed.md}}

当前主题介绍如何在Milvus中创建一个集合。

一个集合由一或多个分区构成。 当创建一个新的集合时，Milvus创建一个默认的分区 `_default`。更多信息参见[Glossary - Collection](glossary.md#Collection)。

下面的例子创建一个两分片[shard](glossary.md#Sharding)的集合，名为`book`, 有一个主键字段名为`book_id`，一个 `INT64`标量字段名为`word_count`, 和一个二维浮点向量字段名为`book_intro`。 真实应用场景往往会使用比这个例子更高维的向量。


## 准备架构

<div class="alert note">
    <ul>
        <li><a href="manage_connection.md">Connecting to Milvus server</a> 在其他操作前确保已连接到Milvus</li>
        <li>创建集合必须包含主键字段与向量字段，INT64是目前Milvus版本主键字段唯一支持的数据类型。</li>
    </ul>
</div>


首先，准备必要参数，包括字段架构，集合架构和集合名。

{{fragments/multiple_code.md}}

```python
from pymilvus import CollectionSchema, FieldSchema, DataType
book_id = FieldSchema(
    name="book_id", 
    dtype=DataType.INT64, 
    is_primary=True, 
    )
word_count = FieldSchema(
    name="word_count", 
    dtype=DataType.INT64,  
    )
book_intro = FieldSchema(
    name="book_intro", 
    dtype=DataType.FLOAT_VECTOR, 
    dim=2
    )
schema = CollectionSchema(
    fields=[book_id, word_count, book_intro], 
    description="Test book search"
    )
collection_name = "book"
```

```javascript
const params = {
  collection_name: "book",
  fields: [
    {
      name: "book_intro",
      description: "",
      data_type: 101,  // DataType.FloatVector
      type_params: {
        dim: "2",
      },
    },
	{
      name: "book_id",
      data_type: 5,   //DataType.Int64
      is_primary_key: true,
      description: "",
    },
    {
      name: "word_count",
      data_type: 5,    //DataType.Int64
      description: "",
    },
  ],
};
```

```cli
create collection -c book -f book_id:INT64 -f word_count:INT64 -f book_intro:FLOAT_VECTOR:2 -p book_id
```

<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Description</th>
            <th>Option</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>FieldSchema</code></td>
            <td>Schema of the fields within the collection to create. Refer to <a href="field_schema.md">Field Schema</a> for more information.</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>name</code></td>
            <td>Name of the field to create.</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>dtype</code></td>
            <td>Data type of the field to create.</td>
            <td>For primary key field:
                <ul>
                    <li><code>DataType.INT64</code> (numpy.int64)</li>
                </ul>
                For scalar field:
                <ul>
                    <li><code>DataType.BOOL</code> (Boolean)</li>
                    <li><code>DataType.INT64</code> (numpy.int64)</li>
                    <li><code>DataType.FLOAT</code> (numpy.float32)</li>
                    <li><code>DataType.DOUBLE</code> (numpy.double)</li>
                </ul>
                For vector field:
                <ul>
                    <li><code>BINARY_VECTOR</code> (Binary vector)</li>
                    <li><code>FLOAT_VECTOR</code> (Float vector)</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>is_primary</code> (Mandatory for primary key field)</td>
            <td>Switch to control if the field is primary key field.</td>
            <td><code>True</code> or <code>False</code></td>
        </tr>
        <tr>
            <td><code>auto_id</code></td>
            <td>Switch to enable or disable Automatic ID (primary key) allocation.</td>
            <td><code>True</code> or <code>False</code></td>
        </tr>
        <tr>
            <td><code>dim</code> (Mandatory for vector field)</td>
            <td>Dimension of the vector.</td>
            <td>[1, 32,768]</td>
        </tr>
        <tr>
            <td><code>description</code> (Optional)</td>
            <td>Description of the field.</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>CollectionSchema</code></td>
        <td>Schema of the collection to create. Refer to <a href="collection_schema.md">Collection Schema</a> for more information.</td>
        </tr>
        <tr>
            <td><code>fields</code></td>
            <td>Fields of the collection to create.</td>
        </tr>
        <tr>
            <td><code>description</code> (Optional)</td>
            <td>Description of the collection to create.</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>collection_name</code></td>
            <td>Name of the collection to create.</td>
        </tr>
	</tbody>
</table>


<table class="language-javascript">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Description</th>
            <th>Option</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>collection_name</code></td>
            <td>Name of the collection to create.</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>description</code></td>
            <td>Description of the collection to create.</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>fields</code></td>
            <td>Schema of the filed and the collection to create.</td>
            <td>Refer to <a href="field_schema.md">Field Schema</a> and <a href="collection_schema.md">Collection Schema</a> for more information.</td>
        </tr>
        <tr>
            <td><code>data_type</code></td>
            <td>Data type of the filed to create.</td>
            <td>Refer to <a href="https://github.com/milvus-io/milvus-sdk-node/blob/main/milvus/types/Common.ts">data type reference number</a> for more information.</td>
        </tr>
        <tr>
            <td><code>is_primary</code> (Mandatory for primary key field)</td>
            <td>Switch to control if the field is primary key field.</td>
            <td><code>True</code> or <code>False</code></td>
        </tr>
        <tr>
            <td><code>auto_id</code></td>
            <td>Switch to enable or disable Automatic ID (primary key) allocation.</td>
            <td><code>True</code> or <code>False</code></td>
        </tr>
        <tr>
            <td><code>dim</code> (Mandatory for vector field)</td>
            <td>Dimension of the vector.</td>
            <td>[1, 32,768]</td>
        </tr>
        <tr>
            <td><code>description</code> (Optional)</td>
            <td>Description of the field.</td>
            <td>N/A</td>
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
            <td>The name of the collection.</td>
        </tr>
        <tr>
            <td>-f (Multiple)</td>
            <td>The field schema in the    ```<fieldName>:<dataType>:<dimOfVector/desc>``` format.</td>
        </tr>
        <tr>
            <td>-p</td>
            <td>The name of the primary key field.</td>
        </tr>
        <tr>
            <td>-a (Optional)</td>
            <td>Flag to generate IDs automatically.</td>
        </tr>
        <tr>
            <td>-d (Optional)</td>
            <td>The description of the collection.</td>
        </tr>
    </tbody>
</table>

## 通过架构创建集合

再者，根据上面定制的架构创建集合。

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection(name=collection_name, schema=schema, using='default', shards_num=2)
```

```javascript
await milvusClient.collectionManager.createCollection(params);
```

```cli
# Follow the previous step.
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
            <td><code>using</code> (optional)</td>
            <td>By specifying the server alias here, you can choose in which Milvus server you create a collection.</td>
        </tr>
        <tr>
            <td><code>shards_num</code> (optional)</td>
            <td>Number of the shards for the collection to create.</td>
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

