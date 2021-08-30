---
id: connect.md
title: Connect
---

# Overview

This section covers fundamentals and basic Milvus operations.

If you choose to operate in the Python interactive mode, type `python3` in your terminal.


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

When you no longer need Milvus services, you can release all connection resources of the Milvus server:

{{fragments/multiple_code.md}}

```python
>>> connections.disconnect("default")
```

```javascript
await milvusClient.closeConnection();
```
