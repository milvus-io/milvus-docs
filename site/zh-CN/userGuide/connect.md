---
id: connect.md
title: 连接服务器
---

# 连接服务器

通过本章节文档，你将在 Python 交互式编程环境下学习 Milvus 使用中的各种基本操作。

命令行输入 `python3` 进入Python 交互式模式。本文以 Python3.9.1 为例：
```
➜  ~ python3
Python 3.9.1 (default, Feb  3 2021, 07:38:02)
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## 连接 Milvus 服务器

{{fragments/multiple_code.md}}


```python
>>> from pymilvus_orm import connections
>>> connections.connect("default", host='localhost', port='19530')
```

```javascript
import { MilvusClient } from "@zilliz/milvus2-sdk-node";
const milvusClient = new MilvusClient("localhost:19530");
```


## 断开与服务器的连接
使用完 Milvus 的服务之后，可以断开与 Milvus 服务器的连接以释放资源：


{{fragments/multiple_code.md}}


```python
>>> connections.disconnect("default")
```

```javascript
await milvusClient.closeConnection();
```
