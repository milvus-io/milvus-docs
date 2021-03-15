---
id: connect_milvus_python.md
---

# 连接服务端

该页面将向你展示如何从 Python 客户端连接 Milvus 服务端。 

<div class="alert note">
<li>关于详细的 API 使用方法，请参考 <a href="https://github.com/milvus-io/pymilvus">Python API 文档</a>。</li>
<li>建议你使用 <a href="https://zilliz.com/sizing-tool">资源评估工具</a> 来估算数据所需的硬件资源。</li>
</div>


1. 导入 pymilvus：

   ```python
   # Import pymilvus.
   >>> from milvus import Milvus, IndexType, MetricType, Status
   ```

2. 使用以下任意一种方法连接 Milvus 服务端：

   ```python
   # Connect to the Milvus server.
   >>> milvus = Milvus(host='localhost', port='19530')
   ```

   <div class="alert note">
   在上面的代码中，<code>host</code> 和 <code>port</code> 都使用了默认值。你可以将其更改为自己设定的 IP 地址和端口。
   </div>

   ```python
   >>> milvus = Milvus(uri='tcp://localhost:19530')
   ```

## 常见问题

<details>
<summary><font color="#4fc4f9">Milvus 的 Python SDK 有连接池吗？</font></summary>
{{fragments/faq_pymilvus_connection_pool.md}}
</details>
<details>
<summary><font color="#4fc4f9">在 Windows 安装 pymilvus 报错，如何解决？</font></summary>
{{fragments/faq_pymilvus_install_error.md}}
</details>
