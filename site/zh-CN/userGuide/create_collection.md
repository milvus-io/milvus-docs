---
id: create_collection.md
related_key: create collection
summary: Learn how to create a collection in Milvus.
---

# 创建 Collection

当前主题介绍如何在 Milvus 中创建 collection。

collection 由一个或多个 partition 构成。collection 被创建时，Milvus 会创建一个默认 partition `_default`，collection 概念详见 [术语表 - 集合](glossary.md#Collection)。

下文的例子创建了一个名为 `book` 的具有两个 [shard](glossary.md#Shard) 的 collection，primary key field 是 `book_id`, 并且包含了类型为 `INT64` 的 `book_id` 标量 field 和 二维浮点数向量 `word_count` filed。真实场景可能会使用比示例更高维的向量。 

Milvus 支持在创建 collection 时设置不同的一致性级别（当前仅 PyMilvus 支持）。本例 collection 的一致性级别被设定为 “强一致性”，意味着 Milvus 会读取在收到搜索或查询请求那一刻的最新数据。若创建 collection 时未指定一致性级别，将默认设置成 “有界一致性”，在搜索或查询请求时，Milvus 会读取近乎最新的数据（通常是几秒前）。除了在创建 collection 时可设置一致性级别外，也可在 [搜索](search.md) 或 [查询](query.md) 时设置一致性级别（当前仅 PyMilvus 支持）。关于 Milvus 支持的其他一致性级别，详见 [Guarantee Timestamp in Search Requests](https://github.com/milvus-io/milvus/blob/master/docs/developer_guides/how-guarantee-ts-works-cn.md).


## 准备 Schema

<div class="alert note">
    <ul>
        <li>在进行任何操作前确保已 <a href="manage_connection.md">连接 Milvus 服务</a>。</li>
        <li>待创建的 collection 必须包含一个 primary key field 和一个向量 field。目前 Milvus 只支持 <code>INT64</code> 类型的 primary key field。</li>
    </ul>
</div>


首先，定义必要的参数，包含 field schema, collection schema 和 collection 名称 。

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
  description: "Test book search"
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

```go
var (
		collectionName = "book"
	)
schema := &entity.Schema{
    CollectionName: collectionName,
    Description:    "Test book search",
    Fields: []*entity.Field{
        {
            Name:       "book_id",
            DataType:   entity.FieldTypeInt64,
            PrimaryKey: true,
            AutoID:     false,
        },
        {
            Name:       "word_count",
            DataType:   entity.FieldTypeInt64,
            PrimaryKey: false,
            AutoID:     false,
        },
        {
            Name:     "book_intro",
            DataType: entity.FieldTypeFloatVector,
            TypeParams: map[string]string{
                "dim": "2",
            },
        },
    },
}
```

```java
FieldType fieldType1 = FieldType.newBuilder()
        .withName("book_id")
        .withDataType(DataType.Int64)
        .withPrimaryKey(true)
        .withAutoID(false)
        .build();
FieldType fieldType2 = FieldType.newBuilder()
        .withName("word_count")
        .withDataType(DataType.Int64)
        .build();
FieldType fieldType3 = FieldType.newBuilder()
        .withName("book_intro")
        .withDataType(DataType.FloatVector)
        .withDimension(2)
        .build();
CreateCollectionParam createCollectionReq = CreateCollectionParam.newBuilder()
        .withCollectionName("book")
        .withDescription("Test book search")
        .withShardsNum(2)
        .addFieldType(fieldType1)
        .addFieldType(fieldType2)
        .addFieldType(fieldType3)
        .build();
```

```shell
create collection -c book -f book_id:INT64 -f word_count:INT64 -f book_intro:FLOAT_VECTOR:2 -p book_id
```

<table class="language-python">
	<thead>
        <tr>
            <th>参数</th>
            <th>描述</th>
            <th>选项</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>FieldSchema</code></td>
            <td>要创建的 collection 内的 fields 的 scheme。 详见 <a href="schema.md">Schema</a>。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>name</code></td>
            <td>要创建的 field 名称。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>dtype</code></td>
            <td>要创建的 field 数据类型。</td>
            <td>对于 primary key field:
                <ul>
                    <li><code>DataType.INT64</code> (numpy.int64)</li>
                </ul>
                对于标量 field:
                <ul>
                    <li><code>DataType.BOOL</code> (Boolean)</li>
                    <li><code>DataType.INT64</code> (numpy.int64)</li>
                    <li><code>DataType.FLOAT</code> (numpy.float32)</li>
                    <li><code>DataType.DOUBLE</code> (numpy.double)</li>
                </ul>
                对于向量 field:
                <ul>
                    <li><code>BINARY_VECTOR</code> (Binary vector)</li>
                    <li><code>FLOAT_VECTOR</code> (Float vector)</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>is_primary</code></td>
            <td>(primary key field 必设) 控制 field 是否为 primary key field。</td>
            <td><code>True</code> 或 <code>False</code></td>
        </tr>
        <tr>
            <td><code>auto_id</code></td>
            <td>(primary key field 必设) 是否开启主键 ID 自动分配</td>
            <td><code>True</code> 或 <code>False</code></td>
        </tr>
        <tr>
            <td><code>dim</code></td>
            <td>(向量必设) 向量维数。</td>
            <td>[1, 32,768]</td>
        </tr>
        <tr>
            <td><code>description</code> </td>
            <td>(可选) field 描述</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>CollectionSchema</code></td>
        <td>要创建的 collection scheme. 详见 <a href="schema.md">Schema</a>。</td>
        <td>N/A</td>
        </tr>
        <tr>
            <td><code>fields</code></td>
            <td>要创建的 collection 的 fields。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>description</code></td>
            <td>(可选) 要创建的 collection 描述。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>collection_name</code></td>
            <td>要创建的 collection 名称。</td>
            <td>N/A</td>
        </tr>
	</tbody>
</table>

<table class="language-go">
	<thead>
        <tr>
            <th>参数</th>
            <th>描述</th>
            <th>选项</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>collectionName</code></td>
            <td>要创建的 collection 名称。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>description</code></td>
            <td>要创建的 collection 描述。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>Fields</code></td>
            <td>要创建的 collection 内的 fields 的 scheme。 详见 <a href="schema.md">Schema</a>。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>Name</code></td>
            <td>要创建的 field 名称。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>DataType</code></td>
            <td>要创建的 field 数据类型。</td>
            <td>对于 primary key field:
                <ul>
                    <li><code>entity.FieldTypeInt64</code> (numpy.int64)</li>
                </ul>
                对于标量 field:
                <ul>
                    <li><code>entity.FieldTypeBool</code> (Boolean)</li>
                    <li><code>entity.FieldTypeInt64</code> (numpy.int64)</li>
                    <li><code>entity.FieldTypeFloat</code> (numpy.float32)</li>
                    <li><code>entity.FieldTypeDouble</code> (numpy.double)</li>
                </ul>
                对于标量 field:
                <ul>
                    <li><code>entity.FieldTypeBinaryVector</code> (Binary vector)</li>
                    <li><code>entity.FieldTypeFloatVector</code> (Float vector)</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PrimaryKey</code></td>
            <td>(primary key field 必设) 控制 field 是否为 primary key field。</td>
            <td><code>True</code> 或 <code>False</code></td>
        </tr>
        <tr>
            <td><code>AutoID</code></td>
            <td>(primary key field 必设) 是否开启主键 ID 自动生成。</td>
            <td><code>True</code> 或 <code>False</code></td>
        </tr>
        <tr>
            <td><code>dim</code></td>
            <td>(向量必设) 向量维数。</td>
            <td>[1, 32768]</td>
        </tr>
	</tbody>
</table>


<table class="language-javascript">
	<thead>
        <tr>
            <th>参数</th>
            <th>描述</th>
            <th>选项</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>collection_name</code></td>
            <td>要创建的 collection 名称。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>description</code></td>
            <td>要创建的 collection 描述。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>fields</code></td>
            <td>要创建的 collection 内的 fields 的 scheme。 </td>
            <td>详见 <a href="schema.md">Schema</a>。</td>
        </tr>
        <tr>
            <td><code>data_type</code></td>
            <td>要创建的 field 数据类型。</td>
            <td>详见 <a href="https://github.com/milvus-io/milvus-sdk-node/blob/main/milvus/types/Common.ts">data type reference number</a> 。</td>
        </tr>
        <tr>
            <td><code>is_primary</code></td>
            <td>(primary key field 必设) 控制 field 是否为 primary key field。</td>
            <td><code>True</code> 或 <code>False</code></td>
        </tr>
        <tr>
            <td><code>auto_id</code></td>
            <td>是否开启主键 ID 自动生成。</td>
            <td><code>True</code> 或 <code>False</code></td>
        </tr>
        <tr>
            <td><code>dim</code> (向量必设)</td>
            <td>向量维数。</td>
            <td>[1, 32768]</td>
        </tr>
        <tr>
            <td><code>description</code> </td>
            <td>(可选) field 描述</td>
            <td>N/A</td>
        </tr>
	</tbody>
</table>

<table class="language-java">
	<thead>
        <tr>
            <th>参数</th>
            <th>描述</th>
            <th>选项</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>Name</code></td>
            <td>要创建的 field 名字。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>Description</code></td>
            <td>要创建的 field 描述。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>DataType</code></td>
            <td>要创建的 field 数据类型。</td>
            <td>对于 primary key field:
                <ul>
                    <li><code>entity.FieldTypeInt64</code> (numpy.int64)</li>
                </ul>
                对于标量 field:
                <ul>
                    <li><code>entity.FieldTypeBool</code> (Boolean)</li>
                    <li><code>entity.FieldTypeInt64</code> (numpy.int64)</li>
                    <li><code>entity.FieldTypeFloat</code> (numpy.float32)</li>
                    <li><code>entity.FieldTypeDouble</code> (numpy.double)</li>
                </ul>
                对于向量 field:
                <ul>
                    <li><code>entity.FieldTypeBinaryVector</code> (Binary vector)</li>
                    <li><code>entity.FieldTypeFloatVector</code> (Float vector)</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PrimaryKey</code></td>
            <td>(primary key field 必设) 控制 field 是否为 primary key field。</td>
            <td><code>True</code> 或 <code>False</code></td>
        </tr>
        <tr>
            <td><code>AutoID</code></td>
            <td>是否开启主键 ID 自动生成。</td>
            <td><code>True</code> 或 <code>False</code></td>
        </tr>
        <tr>
            <td><code>Dimension</code></td>
            <td>(向量必设) 向量维数。</td>
            <td>[1, 32768]</td>
        </tr>
        <tr>
            <td><code>CollectionName</code></td>
            <td>要创建的 collection 名字。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>Description</code></td>
            <td>(可选)要创建的 collection 描述。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>ShardsNum</code></td>
            <td>要创建的 collection 的 shard 数量</td>
            <td>[1,256]</td>
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
            <td>collection 名称。</td>
        </tr>
        <tr>
            <td>-f</td>
            <td>多个使用 <code>&lt;fieldName&gt;:&lt;dataType&gt;:&lt;dimOfVector/desc&gt;</code> 格式的 field schema。</td>
        </tr>
        <tr>
            <td>-p</td>
            <td>primary key field 名称。</td>
        </tr>
        <tr>
            <td>-a </td>
            <td>(可选)是否开启主键 ID 自动生成。</td>
        </tr>
        <tr>
            <td>-d </td>
            <td>(可选)collection 描述。</td>
        </tr>
    </tbody>
</table>

## 使用 schema 创建 collection

然后，使用上面的 schema 以 ”强一致性“ 级别创建 collection

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection(
    name=collection_name, 
    schema=schema, 
    using='default', 
    shards_num=2,
    consistency_level="Strong"
    )
```

```javascript
await milvusClient.collectionManager.createCollection(params);
```

```go
err = milvusClient.CreateCollection(
    context.Background(), // ctx
    schema,
    2, // shardNum
)
if err != nil {
    log.Fatal("failed to create collection:", err.Error())
}
```

```java
milvusClient.createCollection(createCollectionReq);
```

```shell
# Follow the previous step.
```

<table class="language-python">
	<thead>
        <tr>
            <th>参数</th>
            <th>描述</th>
            <th>选项</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>using</code></td>
            <td>(可选) 通过在这里定义 Milvus 服务器别名，你可以选择在哪个 Milvus 服务器创建 collection。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>shards_num</code></td>
            <td>(可选) 要创建的 collection 的 shard 数量。</td>
            <td>[1,256]</td>
        </tr>
        <tr>
            <td><code>consistency_level</code></td>
            <td>(可选)要创建的 collection 的一致性级别。</td>
            <td>
                <ul>
                    <li><code>Strong</code></li>
                    <li><code>Bounded</code></li>
                    <li><code>Session</code></li>
                    <li><code>Eventually</code></li>
                    <li><code>Customized</code></li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

<table class="language-go">
	<thead>
        <tr>
            <th>参数</th>
            <th>描述</th>
            <th>选项</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>ctx</code></td>
            <td>控制调用 API 的 Context。</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>shardNum</code></td>
            <td>要创建的 collection 的 shard 数量。</td>
            <td>[1,256]</td>
        </tr>
    </tbody>
</table>



## 使用限制
| 类型                            | 最大长度   |
|-------------------------------|--------|
| collection 名称长度               | 255 字符 |
| 每个 collection 的 partition 数量  | 4,096  |
| 每个 collection 的 field 数量      | 256    |
| 每个 collection 的 shard 数量      | 256    |



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

