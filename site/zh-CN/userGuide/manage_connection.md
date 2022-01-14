---
id: manage_connection.md
related_key: connect Milvus
summary: Learn how to connect to a Milvus server.
---

# Manage Milvus Connections

{{fragments/translation_needed.md}}

This topic describes how to connect to and disconnect from a Milvus server.

<div class="alert note">
  Ensure to connect to Milvus server before any operations.
</div>

Below example connects to a Milvus server with host as `localhost` and port as `19530` and disconnects from it.


## Connect to a Milvus server

Construct a Milvus connection. Ensure to connect to Milvus server before any operations.

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
		<th>Parameter</th>
		<th>Description</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>alias</code></td>
		<td>Alias of the Milvus connection to construct.</td>
	</tr>
	<tr>
		<td><code>host</code></td>
		<td>IP address of the Milvus server.</td>
	</tr>
	<tr>
		<td><code>port</code></td>
		<td>Port of the Milvus server.</td>
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
	    	<td><code>address</code></td>
		<td>Address of the Milvus connection to construct.</td>
	</tr>
	</tbody>
</table>

<table class="language-cli">
    <thead>
        <tr>
            <th>Option</th>
            <th>Full name</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>-h</td>
            <td>--host</td>
            <td>(Optional) The host name. The default is "127.0.0.1".</td>
        </tr>
        <tr>
            <td>-p</td>
            <td>--port</td>
            <td>(Optional) The port number. The default is "19530".</td>
        </tr>
        <tr>
            <td>-a</td>
            <td>--alias</td>
            <td>(Optional) The alias name of the Milvus link. The default is "default".</td>
        </tr>
        <tr>
            <td>-D</td>
            <td>--disconnect</td>
            <td>(Optional) Flag to disconnect from the Milvus server specified by an alias. The default alias is "default".</td>
        </tr>
        <tr>
            <td>--help</td>
            <td>n/a</td>
            <td>Displays help for using the command.</td>
        </tr>
    </tbody>
</table>

## Disconnect from a Milvus server

Disconnect from a Milvus server.

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
		<th>Parameter</th>
		<th>Description</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>alias</code></td>
		<td>Alias of the Milvus server to disconnect from.</td>
	</tr>
	</tbody>
</table>

## What's next

Having connected to a Milvus server, you can:

- [Create a collection](create_collection.md)
- [Manage data](insert_data.md)
- [Build a vector index](build_index.md)
- [Conduct a vector search](search.md)
- [Conduct a hybrid search](hybridsearch.md)

For advanced operations, check:

- [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
- [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

