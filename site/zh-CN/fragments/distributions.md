Milvus 提供两个发行版本：CPU 版本和 GPU 版本。

<ul>
<li>CPU 版 Milvus 仅支持搜索计算在创建索引结束后进行，更适合静态数据。</li>
<li>GPU 版 Milvus 在 CPU 版的基础上进行了 GPU 加速：支持同时进行索引创建和搜索计算以提高查询效率，适合动态增加的数据。</li>
</ul>

如果你的计算机上安装了支持 CUDA 功能的 GPU 设备，你可以安装 Milvus 的 GPU 版本以获取针对海量数据的更优的查询性能。