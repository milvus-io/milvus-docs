---
id: connect.md
title: Connect
---

# Overview

This section covers fundamentals and basic Milvus operations in Python interactive mode.

Type `python3` in your terminal to enter Python interactive mode. Here we take Python 3.9.1 as an example:

```
➜  ~ python3
Python 3.9.1 (default, Feb  3 2021, 07:38:02)
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## Connect to the Milvus server

{{fragments/multiple_code.md}}

```python
>>> from pymilvus_orm import connections
>>> connections.connect("default", host='localhost', port='19530')
```

```javascript
import { MilvusClient } from "@zilliz/milvus2-sdk-node";
const milvusClient = new MilvusClient("localhost:19530");
```

## Disconnect from the Milvus server

When you no longer need Milvus services, you can call `disconnect()` to release all connection resources to the Milvus server:

{{fragments/multiple_code.md}}

```python
>>> connections.disconnect("default")
```

```javascript
await milvusClient.closeConnection();
```
