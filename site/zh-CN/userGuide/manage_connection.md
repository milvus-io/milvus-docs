---
id: manage_connection.md
related_key: connect Milvus
summary: Learn how to connect to a Milvus server.
---

# 管理Milvus连接

{{fragments/translation_needed.md}}

当前主题介绍怎么连接、断开 Milvus 服务器。

<div class="alert note">
  在进行其他操作前确保连接到 Milvus 服务器。
</div>

下面的例子使用 `localhost` 作为主机名，端口号 `19530` 展示连接或断开连接到 Milvus 服务器。


## 连接到 Milvus 服务器

构建一个 Milvus 连接。在进行其他操作前确保已连接 Milvus 服务。

{{fragments/multiple_code.md}}

```python
# Run `python3` in your terminal to operate in the Python interactive mode.
from pymilvus import connections
connections.connect(alias="default", host='localhost', port='19530')
```

```javascript
import { MilvusClient } from "@zilliz/milvus2-sdk-node";
const address = "localhost:19530";
const milvusClient = new MilvusClient(address);
```

```cli
connect -h localhost -p 19530 -a default
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
		<td><code>alias</code></td>
		<td>创建的Milvus连接的别名。</td>
	</tr>
	<tr>
		<td><code>host</code></td>
		<td>Milvus 服务 IP 地址。</td>
	</tr>
	<tr>
		<td><code>port</code></td>
		<td>Milvus 服务端口号。</td>
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
	    	<td><code>address</code></td>
		<td>Milvus 服务地址。</td>
	</tr>
	</tbody>
</table>

<table class="language-cli">
    <thead>
        <tr>
            <th>选项</th>
            <th>全称</th>
            <th>描述</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>-h</td>
            <td>--host</td>
            <td>(可选) Milvus 服务 IP 地址。默认为 "127.0.0.1"。</td>
        </tr>
        <tr>
            <td>-p</td>
            <td>--port</td>
            <td>(可选) Milvus 服务端口。默认为 "19530"。</td>
        </tr>
        <tr>
            <td>-a</td>
            <td>--alias</td>
            <td>(可选) Milvus 链接别名。默认为 "default"。</td>
        </tr>
        <tr>
            <td>-D</td>
            <td>--disconnect</td>
            <td>(可选) 使用别名断开链接的标记。默认别名为  "default".</td>
        </tr>
        <tr>
            <td>--help</td>
            <td>n/a</td>
            <td>显示命令行帮助</td>
        </tr>
    </tbody>
</table>

## 断开 MIlvus 连接

从 MIlvus 服务器断开。

{{fragments/multiple_code.md}}

```python
connections.disconnect("default")
```


```javascript
await milvusClient.closeConnection();
```

```cli
connect -D
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
		<td><code>alias</code></td>
		<td>Milvus 服务别名。</td>
	</tr>
	</tbody>
</table>

## What's next

链接 Milvus 后，还可以：

- [创建 collection](create_collection.md)
- [插入数据](insert_data.md)
- [创建索引](build_index.md)
- [向量搜索](search.md)
- [混合搜索](hybridsearch.md)

关于其他操作，参考

- [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
- [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

