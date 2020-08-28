<div class="alert note">
<ul>
<li>如果你的主机由于网络限制无法在线获得 Docker 镜像和配置文件，请从其他主机在线获取镜像，保存为 TAR 文件传输回本地，传输完成后重新加载为 Docker 镜像：
<details>
<summary><font color="#3ab7f8">点击查看离线传输相关代码示例。</font></summary>
<ol>
 <li>将 Docker 镜像保存为 TAR 文件再使用合适的方式传输。</br>

<code class="language-shell">
    $ docker save milvusdb/milvus > milvus_image.tar
</code>
</li>

<li>将 TAR 文件传输完成后使用以下命令重新加载成 Docker 镜像。</br>

<code class="language-shell">
    $ docker load < milvus_image.tar
</code>
</li></ol>
</details></li>
<li>如果拉取镜像的速度过慢或一直失败，请参考 <a href="operational_faq.md">操作常见问题</a> 中提供的解决办法。</li>
</ul>
</div>