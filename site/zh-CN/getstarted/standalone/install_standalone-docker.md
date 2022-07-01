---
id: install_standalone-docker.md
label: Docker Compose 安装
order: 0
group: install_standalone-docker.md
---

# 安装 Milvus 单机版

{{fragments/installation_guide.md}}


{{tab}}


## 安装 Milvus 单机版


1. 下载 **milvus-standalone-docker-compose.yml** 配置文件并保存为 **docker-compose.yml**
```
wget https://github.com/milvus-io/milvus/releases/download/v{{var.milvus_release_tag}}/milvus-standalone-docker-compose.yml -O docker-compose.yml
```
> 你可以在 GitHub 直接 [下载](https://github.com/milvus-io/milvus/releases/download/v{{var.milvus_release_tag}}/milvus-standalone-docker-compose.yml) **docker-compose.yml**。

<div class="alert note">
如果你使用原始 <b>docker-compose.yml</b> 文件安装 Milvus, 数据将会被存储在 <b>./volume</b> 路径下。如需修改映射路径，你可以直接修改 <b>docker-compose.yml</b> 文件，或运行 <code>$ export DOCKER_VOLUME_DIRECTORY=</code>。
</div>

2. 启动 Milvus 单机版：

```shell
$ sudo docker-compose up -d
```

```text
Docker Compose is now in the Docker CLI, try `docker compose up`
Creating milvus-etcd  ... done
Creating milvus-minio ... done
Creating milvus-standalone ... done
```

*如果 Milvus 单机版启动正常，可以看到有 3 个 Docker 容器在运行（2 个为基础服务，1 个为 Milvus 服务）：*

```
$ sudo docker-compose ps
      Name                     Command                  State                          Ports
----------------------------------------------------------------------------------------------------------------
milvus-etcd         etcd -listen-peer-urls=htt ...   Up (healthy)   2379/tcp, 2380/tcp
milvus-minio        /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp
milvus-standalone   /tini -- milvus run standalone   Up             0.0.0.0:19530->19530/tcp,:::19530->19530/tcp
```

<div class="alert note">
运行 <code>$ sudo docker-compose down</code> 停止 Milvus 单机版。

如果你想在停止Milvus后清理数据，运行 <code>$ sudo rm -rf  volume</code>。

</div>

<div class="alert note">
阅读 <a href="upgrade.md">升级指南 2.0</a> 了解如何升级 Milvus 2.0 版本。
</div>
