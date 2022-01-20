---
id: timetravel.md
related_key: Time Travel
summary: Learn how to search with Time Travel in Milvus.
---

# 使用 Time Travel搜索

{{fragments/translation_needed.md}}

本章描述怎么在向量个搜索中使用Time Travel搜索特性。

Milvus维护所有数据插入和删除操作的时间线。 它允许用户在搜索中指定时间戳以在指定时间点检索数据视图，而无需在数据回滚的维护上花费大量资金。

<div class="alert note">
默认情况下, Milvus允许Time Travel跨度432,000秒(120h0m0s)。您可在<code>common.retentionDuration</code>配置这个参数。
</div>

## 准备工作

下面的样例代码示范了插入数据前的步骤。

如您在已有的Milvus实例中使用自己的数据集，跳到下一步。

{{fragments/multiple_code.md}}

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
connections.connect("default", host='localhost', port='19530')
collection_name = "test_time_travel"
schema = CollectionSchema([
    FieldSchema("pk", DataType.INT64, is_primary=True),
    FieldSchema("example_field", dtype=DataType.FLOAT_VECTOR, dim=2)
])
collection = Collection(collection_name, schema)
```

```javascript
const { MilvusClient } =require("@zilliz/milvus2-sdk-node");
const milvusClient = new MilvusClient("localhost:19530");
const params = {
  collection_name: "test_time_travel",
  fields: [{
      name: "example_field",
      description: "",
      data_type: 101, // DataType.FloatVector
      type_params: {
        dim: "2",
      },
    },
    {
      name: "pk",
      data_type: 5, //DataType.Int64
      is_primary_key: true,
      description: "",
    },
  ],
};
await milvusClient.collectionManager.createCollection(params);
```

```cli
connect -h localhost -p 19530 -a default
create collection -c test_time_travel -f pk:INT64:primary_field -f example_field:FLOAT_VECTOR:2 -p pk
```

## 插入首批数据

插入随机数据来模拟原始数据（MIlvus CLI例子使用一个包含类似数据的预构建、远端CSV文件）。

{{fragments/multiple_code.md}}

```python
import random
data = [
    [i for i in range(10)],
    [[random.random() for _ in range(2)] for _ in range(10)],
]
batch1 = collection.insert(data)
```

```javascript
const entities1 = Array.from({ length: 10 }, (v, k) => ({
  "example_field": Array.from({   length: 2  }, () => Math.random()),
  "pk": k,
}));
const batch1 = milvusClient.dataManager.insert({
  collection_name: "test_time_travel",
  fields_data: entities1,
});
```

```cli
import -c test_time_travel https://raw.githubusercontent.com/zilliztech/milvus_cli/main/examples/user_guide/search_with_timetravel_1.csv
Reading file from remote URL.
Reading csv rows...  [####################################]  100%
Column names are ['pk', 'example_field']
Processed 11 lines.

Inserted successfully.

--------------------------  ------------------
Total insert entities:                      10
Total collection entities:                  10
Milvus timestamp:           430390410783752199
--------------------------  ------------------
```

## 检查首批数据的时间戳

使用Time Travel来检查询首批数据的时间戳。同一批插入数据共享一个相同的时间戳。

```python
batch1.timestamp
428828271234252802
```

```javascript
batch1.timestamp
428828271234252802
```

```cli
# Milvus CLI automatically returns the timestamp as shown in the previous step.
```

<div class="alert note">
  Milvus 采用物理时钟和逻辑计数器的组合作为混合时间戳。64位时间戳由46位物理部分（高位）和18位逻辑部分（低位）组成。物理部分是自1970年1月1日（UTC/GMT午夜）以来经过的毫秒数。
</div>



## 插入第二批数据

插入第二批数据来模拟脏数据，其中追加一条主键值为‘19’向量值为‘[1.0,1.0]’的数据作为后面查询步骤的目标数据（MIlvus CLI例子使用一个包含类似数据的预构建、远端CSV文件）。

{{fragments/multiple_code.md}}

```python
data = [
    [i for i in range(10, 20)],
    [[random.random() for _ in range(2)] for _ in range(9)],
]
data[1].append([1.0,1.0])
batch2 = collection.insert(data)
```

```javascript
const entities2 = Array.from({
  length: 9
}, (v, k) => ({
  "example_field": Array.from({
    length: 2
  }, () => Math.random()),
  "pk": k + 10,
}));
entities2.push({
  "pk": 19,
  "example_field": [1.0, 1.0],
});
const batch2 = await milvusClient.dataManager.insert({
  collection_name: "test_time_travel",
  fields_data: entities2,
});
```

```cli
import -c test_time_travel https://raw.githubusercontent.com/zilliztech/milvus_cli/main/examples/user_guide/search_with_timetravel_2.csv
Reading file from remote URL.
Reading csv rows...  [####################################]  100%
Column names are ['pk', 'example_field']
Processed 11 lines.

Inserted successfully.

--------------------------  ------------------
Total insert entities:                      10
Total collection entities:                  20
Milvus timestamp:           430390435713122310
--------------------------  ------------------
```

## 使用特定的时间戳来查询

加载集合，使用首批数据的时间戳来查询目标数据。因时间戳具体规定，Milvus只获取到指向那个时间戳的数据。

{{fragments/multiple_code.md}}

```python
collection.load()
search_param = {
    "data": [[1.0, 1.0]],
    "anns_field": "example_field",
    "param": {"metric_type": "L2"},
    "limit": 10,
    "travel_timestamp": batch1.timestamp,
}
res = collection.search(**search_param)
res[0].ids
```

```javascript
await milvusClient.collectionManager.loadCollection({
  collection_name: "test_time_travel",
});
const res = await milvusClient.dataManager.search({
  collection_name: "test_time_travel",
  vectors: [
    [1.0, 1.0]
  ],
  travel_timestamp: batch1.timestamp,
  search_params: {
    anns_field: "example_field",
    topk: "10",
    metric_type: "L2",
    params: JSON.stringify({
      nprobe: 10
    }),
  },
  vector_type: 101, // DataType.FloatVector,
});
console.log(res1.results)
```

```cli
search
Collection name (test_collection_query, test_time_travel): test_time_travel
The vectors of search data (the length of data is number of query (nq), the dim of every vector in data must be equal to vector field’s of collection. You can also import a CSV file without headers): [[1.0, 1.0]]
The vector field used to search of collection (example_field): example_field
The specified number of decimal places of returned distance [-1]: 
The max number of returned record, also known as topk: 10
The boolean expression used to filter attribute []: 
The names of partitions to search (split by "," if multiple) ['_default'] []: 
Timeout []: 
Guarantee Timestamp(It instructs Milvus to see all operations performed before a provided timestamp. If no such timestamp is provided, then Milvus will search all operations performed to date) [0]: 
Travel Timestamp(Specify a timestamp in a search to get results based on a data view) [0]: 430390410783752199
```

如下所示，目标数据自己与第二批插入的数据都没有出现在结果中。

```python
[8, 7, 4, 2, 5, 6, 9, 3, 0, 1]
```

```javascript
[8, 7, 4, 2, 5, 6, 9, 3, 0, 1]
```

```cli
Search results:

No.1:
+---------+------+------------+-----------+
|   Index |   ID |   Distance |     Score |
+=========+======+============+===========+
|       0 |    2 |  0.0563737 | 0.0563737 |
+---------+------+------------+-----------+
|       1 |    5 |  0.122474  | 0.122474  |
+---------+------+------------+-----------+
|       2 |    3 |  0.141737  | 0.141737  |
+---------+------+------------+-----------+
|       3 |    8 |  0.331008  | 0.331008  |
+---------+------+------------+-----------+
|       4 |    0 |  0.618705  | 0.618705  |
+---------+------+------------+-----------+
|       5 |    1 |  0.676788  | 0.676788  |
+---------+------+------------+-----------+
|       6 |    9 |  0.69871   | 0.69871   |
+---------+------+------------+-----------+
|       7 |    6 |  0.706456  | 0.706456  |
+---------+------+------------+-----------+
|       8 |    4 |  0.956929  | 0.956929  |
+---------+------+------------+-----------+
|       9 |    7 |  1.19445   | 1.19445   |
+---------+------+------------+-----------+
```

如您不指定时间戳或者指定为第二批数据的时间戳，MIlvus将从先后两批数据中返回查询结果。

{{fragments/multiple_code.md}}

```python
batch2.timestamp
428828283406123011
search_param = {
    "data": [[1.0, 1.0]],
    "anns_field": "example_field",
    "param": {"metric_type": "L2"},
    "limit": 10,
    "travel_timestamp": batch2.timestamp,
}
res = collection.search(**search_param)
res[0].ids
[19, 10, 8, 7, 4, 17, 2, 5, 13, 15]
```

```javascript
batch2.timestamp
428828283406123011
const res2 = await milvusClient.dataManager.search({
  collection_name: "test_time_travel",
  vectors: [
    [1.0, 1.0]
  ],
  travel_timestamp: batch2.timestamp,
  search_params: {
    anns_field: "example_field",
    topk: "10",
    metric_type: "L2",
    params: JSON.stringify({
      nprobe: 10
    }),
  },
  vector_type: 101, // DataType.FloatVector,
});
console.log(res2.results)
```

```cli
search 
Collection name (test_collection_query, test_time_travel): test_time_travel
The vectors of search data (the length of data is number of query (nq), the dim of every vector in data must be equal to vector field’s of collection. You can also import a CSV file without headers): [[1.0, 1.0]]
The vector field used to search of collection (example_field): example_field
The specified number of decimal places of returned distance [-1]: 
The max number of returned record, also known as topk: 10
The boolean expression used to filter attribute []: 
The names of partitions to search (split by "," if multiple) ['_default'] []: 
Timeout []: 
Guarantee Timestamp(It instructs Milvus to see all operations performed before a provided timestamp. If no such timestamp is provided, then Milvus will search all operations performed to date) [0]: 
Travel Timestamp(Specify a timestamp in a search to get results based on a data view) [0]: 
Search results:

No.1:
+---------+------+------------+------------+
|   Index |   ID |   Distance |      Score |
+=========+======+============+============+
|       0 |   19 | 0          | 0          |
+---------+------+------------+------------+
|       1 |   12 | 0.00321393 | 0.00321393 |
+---------+------+------------+------------+
|       2 |    2 | 0.0563737  | 0.0563737  |
+---------+------+------------+------------+
|       3 |    5 | 0.122474   | 0.122474   |
+---------+------+------------+------------+
|       4 |    3 | 0.141737   | 0.141737   |
+---------+------+------------+------------+
|       5 |   10 | 0.238646   | 0.238646   |
+---------+------+------------+------------+
|       6 |    8 | 0.331008   | 0.331008   |
+---------+------+------------+------------+
|       7 |   18 | 0.403166   | 0.403166   |
+---------+------+------------+------------+
|       8 |   13 | 0.508617   | 0.508617   |
+---------+------+------------+------------+
|       9 |   11 | 0.531529   | 0.531529   |
+---------+------+------------+------------+
```

## 生成时间戳来查询

在没有记录之前时间戳的情况下，Milvus允许您使用现有的时间戳，Unix纪元时间，或者日期时间来生成时间戳。

下面的例子模拟意外删除操作，展示如何生成一个先于删除操作的时间戳来查询到数据。

依据日期时间或者Unix纪元时间生成先于删除操作的时间戳。

```python
import datetime
datetime = datetime.datetime.now()
from pymilvus import utility
pre_del_timestamp = utility.mkts_from_datetime(datetime)
```

```javascript
const {  datetimeToHybrids } = require("@zilliz/milvus2-sdk-node/milvus/utils/Format");
const datetime = new Date().getTime()
const pre_del_timestamp = datetimeToHybrids(datetime)
```

```cli
calc mkts_from_unixtime -e 1641809375
430390476800000000
```

删除部分数据来模拟意外删除操作。

```python
expr = "pk in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]"
collection.delete(expr)
```

```javascript
const expr = "pk in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]"
await milvusClient.dataManager.deleteEntities({
  collection_name: "test_time_travel",
  expr: expr,
});
```

```cli
delete entities -c test_time_travel
The expression to specify entities to be deleted, such as "film_id in [ 0, 1 ]": pk in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
You are trying to delete the entities of collection. This action cannot be undone!

Do you want to continue? [y/N]: y
(insert count: 0, delete count: 10, upsert count: 0, timestamp: 430390494161534983)
```

如下所示，删除部分数据没有在结果中返回如查询不指定时间戳。

```python
search_param = {
    "data": [[1.0, 1.0]],
    "anns_field": "example_field",
    "param": {"metric_type": "L2"},
    "limit": 10,
}
res = collection.search(**search_param)
res[0].ids
```

```javascript
const res3 = await milvusClient.dataManager.search({
  collection_name: "test_time_travel",
  vectors: [
    [1.0, 1.0]
  ],
  search_params: {
    anns_field: "example_field",
    topk: "10",
    metric_type: "L2",
    params: JSON.stringify({
      nprobe: 10
    }),
  },
  vector_type: 101, // DataType.FloatVector,
});
console.log(res3.results)
```

```cli
search 
Collection name (test_collection_query, test_time_travel): test_time_travel
The vectors of search data (the length of data is number of query (nq), the dim of every vector in data must be equal to vector field’s of collection. You can also import a CSV file without headers): [[1.0, 1.0]]
The vector field used to search of collection (example_field): example_field
The specified number of decimal places of returned distance [-1]: 
The max number of returned record, also known as topk: 10
The boolean expression used to filter attribute []: 
The names of partitions to search (split by "," if multiple) ['_default'] []: 
Timeout []: 
Guarantee Timestamp(It instructs Milvus to see all operations performed before a provided timestamp. If no such timestamp is provided, then Milvus will search all operations performed to date) [0]: 
Travel Timestamp(Specify a timestamp in a search to get results based on a data view) [0]: 
Search results:

No.1:
+---------+------+------------+----------+
|   Index |   ID |   Distance |    Score |
+=========+======+============+==========+
|       0 |   19 |   0        | 0        |
+---------+------+------------+----------+
|       1 |    5 |   0.122474 | 0.122474 |
+---------+------+------------+----------+
|       2 |    3 |   0.141737 | 0.141737 |
+---------+------+------------+----------+
|       3 |   13 |   0.508617 | 0.508617 |
+---------+------+------------+----------+
|       4 |   11 |   0.531529 | 0.531529 |
+---------+------+------------+----------+
|       5 |   17 |   0.593702 | 0.593702 |
+---------+------+------------+----------+
|       6 |    1 |   0.676788 | 0.676788 |
+---------+------+------------+----------+
|       7 |    9 |   0.69871  | 0.69871  |
+---------+------+------------+----------+
|       8 |    7 |   1.19445  | 1.19445  |
+---------+------+------------+----------+
|       9 |   15 |   1.53964  | 1.53964  |
+---------+------+------------+----------+
```

使用删除操作前的时间戳，Milvus会返回删除前的数据。

```python
search_param = {
    "data": [[1.0, 1.0]],
    "anns_field": "example_field",
    "param": {"metric_type": "L2"},
    "limit": 10,
    "travel_timestamp": pre_del_timestamp,
}
res = collection.search(**search_param)
res[0].ids
```

```javascript
const res4 = await milvusClient.dataManager.search({
  collection_name: "test_time_travel",
  vectors: [
    [1.0, 1.0]
  ],
  travel_timestamp: pre_del_timestamp,
  search_params: {
    anns_field: "example_field",
    topk: "10",
    metric_type: "L2",
    params: JSON.stringify({
      nprobe: 10
    }),
  },
  vector_type: 101, // DataType.FloatVector,
});
console.log(res4.results)
```

```cli
search 
Collection name (test_collection_query, test_time_travel): test_time_travel
The vectors of search data (the length of data is number of query (nq), the dim of every vector in data must be equal to vector field’s of collection. You can also import a CSV file without headers): [[1.0, 1.0]]
The vector field used to search of collection (example_field): example_field
The specified number of decimal places of returned distance [-1]: 
The max number of returned record, also known as topk: 10
The boolean expression used to filter attribute []: 
The names of partitions to search (split by "," if multiple) ['_default'] []: 
Timeout []: 
Guarantee Timestamp(It instructs Milvus to see all operations performed before a provided timestamp. If no such timestamp is provided, then Milvus will search all operations performed to date) [0]: 
Travel Timestamp(Specify a timestamp in a search to get results based on a data view) [0]: 430390476800000000
Search results:

No.1:
+---------+------+------------+------------+
|   Index |   ID |   Distance |      Score |
+=========+======+============+============+
|       0 |   19 | 0          | 0          |
+---------+------+------------+------------+
|       1 |   12 | 0.00321393 | 0.00321393 |
+---------+------+------------+------------+
|       2 |    2 | 0.0563737  | 0.0563737  |
+---------+------+------------+------------+
|       3 |    5 | 0.122474   | 0.122474   |
+---------+------+------------+------------+
|       4 |    3 | 0.141737   | 0.141737   |
+---------+------+------------+------------+
|       5 |   10 | 0.238646   | 0.238646   |
+---------+------+------------+------------+
|       6 |    8 | 0.331008   | 0.331008   |
+---------+------+------------+------------+
|       7 |   18 | 0.403166   | 0.403166   |
+---------+------+------------+------------+
|       8 |   13 | 0.508617   | 0.508617   |
+---------+------+------------+------------+
|       9 |   11 | 0.531529   | 0.531529   |
+---------+------+------------+------------+
```

## 下一步


- 学习更多Milvus基础操作：
  - [Query vectors](query.md)
  - [Conduct a hybrid search](hybridsearch.md)
- 探索Milvus SDK的API参考：
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)
