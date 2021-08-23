---
id: query.md
title: 结构化匹配
---

# 结构化匹配

Milvus 除了支持存储向量数据外，还支持存储 bool、int、float 等类型的结构化数据，并且提供了结构化数据的匹配功能。结构化匹配是一个全量检索的过程，Milvus 会返回满足条件的所有数据。结构化匹配使用[布尔表达式（boolean expression）](https://milvus.io/cn/docs/v2.0.0/boolean.md)来表示匹配条件。

1. 连接至 Milvus 服务器：


{{fragments/multiple_code.md}}


```python
>>> from pymilvus_orm import connections
>>> connections.connect("default", host='localhost', port='19530')
```



```javascript
//TODO
```

2. 准备 collection 参数并创建 collection：


{{fragments/multiple_code.md}}

```python
>>> from pymilvus_orm import Collection, FieldSchema, CollectionSchema, DataType
>>> collection_name = "test_collection_search"
>>> schema = CollectionSchema([
...     FieldSchema("film_id", DataType.INT64, is_primary=True),
...     FieldSchema("film_date", DataType.INT64),
...     FieldSchema("films", dtype=DataType.FLOAT_VECTOR, dim=2)
... ])
>>> collection = Collection(collection_name, schema)
```



```javascript
//TODO
```

3. 随机生成向量数据并插入新建 collection 中：


{{fragments/multiple_code.md}}


```python
>>> import random
>>> data = [
...     [i for i in range(10)],
...     [1990 + i for i in range(10)],
...     [[random.random() for _ in range(2)] for _ in range(10)],
... ]
>>> collection.insert(data)
>>> collection.num_entities
10
```



```javascript
//TODO
```

4. 将集合加载到内存中并进行结构化匹配：


{{fragments/multiple_code.md}}


```python
>>> collection.load()
>>> expr = "film_id in [2,4,6,8]"
>>> output_fields = ["film_id", "film_date"]
>>> res = collection.query(expr, output_fields)
```



```javascript
//TODO
```

5. 检查返回结果：


{{fragments/multiple_code.md}}

```python
>>> sorted_res = sorted(res, key=lambda k: k['film_id']) 
>>> sorted_res
[{'film_id': 2, 'film_date': 1992},
 {'film_id': 4, 'film_date': 1994},
 {'film_id': 6, 'film_date': 1996},
 {'film_id': 8, 'film_date': 1998}]
```



```javascript
//TODO
```

