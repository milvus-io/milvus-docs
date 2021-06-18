---
id: install_cluster-docker.md
title: 安装 Milvus 分布式版
label: 使用 Docker 安装
order: 0
group: cluster
---
# 安装 Milvus 分布式版

## 开始之前

请先检查你的 Docker、Docker Compose 及硬件设备是否满足 Milvus 安装要求。

<details><summary>检查 Docker 及 Docker Compose 版本：</summary>

<div class="alert note">
建议使用 Docker Compose 安装 Milvus 分布式版。
</div>

- 运行 `$ sudo docker info` 确认 Docker 版本。建议使用 19.03 或以上版本。

> 安装 Docker 步骤见 [Docker CE/EE 官方安装说明](https://docs.docker.com/get-docker/)。

- 运行 `$ sudo docker-compose version` 确认 Docker Compose 版本。建议使用 1.25.1 或以上版本。 

> 安装 Docker Compose 步骤见 [Docker Compose 官方安装说明](https://docs.docker.com/compose/install/)。
</details>

<details><summary>检查 CPU 是否支持 SIMD 扩展指令集合：</summary>

Milvus 在构建索引和查询向量时依赖 CPU 对 SIMD (Single Instruction Multiple Data) 扩展指令集合的支持。请确保运行 Milvus 的 CPU 至少支持以下一种 SIMD 指令集合：

- SSE4.2
- AVX
- AVX2
- AVX512

使用 lscpu 命令以检查 CPU 是否支持特定 SIMD 指令集合：
```
$ lscpu | grep -e sse4_2 -e avx -e avx2 -e avx512
```

</details>

<details><summary>检查 GPU 的计算能力：</summary>
Milvus 对于浮点型向量支持 GPU 加速。Milvus 默认支持的 Nvidia GPU 算力版本为 6.0、6.1、7.0、7.5。

> 你可以[根据 GPU 的型号查询对应的算力版本](https://developer.nvidia.com/zh-cn/cuda-gpus#compute)。

Milvus 要求 [CUDA 10.0 或以上版本](https://developer.nvidia.com/cuda-10.0-download-archive)。

> 在 Milvus 中启用 GPU 加速是可选的。如果硬件环境中没有 GPU，你依然可以运行完整的 Milvus 服务。

在当前的 Milvus 版本中，以下索引类型支持 GPU 加速：
- FLAT
- IVF_FLAT
- IVF_SQ8
- IVF_PQ

更多关于 Milvus 中的索引，详见[向量索引](index.md)。
</details>

## 安装 Milvus 分布式版

{{tab}}

1. 下载 Docker Compose 配置文件 **docker-compose.yml**：

```
$ mkdir -p /home/$USER/milvus
$ cd home/$USER/milvus
$ wget https://raw.githubusercontent.com/milvus-io/milvus/v2.0.0/deployments/docker/distributed/docker-compose.yml
```


2. 启动 Docker Compose：

```
$ sudo docker-compose up -d 
```

*如果所有服务启动正常，可以看到有 12 个 docker 容器在运行（9 个为基础服务，3 个为 Milvus 服务）*


<code>
$ sudo docker ps 

<table>
    <tr>
        <td>CONTAINER ID</td>
        <td>IMAGE</td>
        <td>COMMAND</td>
        <td>CREATED</td>
        <td>STATUS</td>
        <td>PORTS</td>
        <td>NAMES</td>
    </tr>
    <tr>
        <td>0f9d37d78e0c</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_querynode_1</td>
    </tr>
    <tr>
        <td>40568c5d5c40</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_indexnode_1</td>
    </tr>
    <tr>
        <td>071124ad8e1a</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_datanode_1</td>
    </tr>
    <tr>
        <td>22d4786a6b22</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td>0.0.0.0:19530-&gt;19530/tcp, :::19530-&gt;19530/tcp</td>
        <td>distributed_proxynode_1</td>
    </tr>
    <tr>
        <td>f92daa379628</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_indexservice_1</td>
    </tr>
    <tr>
        <td>5d592010b3aa</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_master_1</td>
    </tr>
    <tr>
        <td>481bae1480ea</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_queryservice_1</td>
    </tr>
    <tr>
        <td>d87fe6b9d731</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_proxyservice_1</td>
    </tr>
    <tr>
        <td>7513e26e1ee2</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus/bi…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_dataservice_1</td>
    </tr>
    <tr>
        <td>75d4ff2916b7</td>
        <td>minio/minio:RELEASE.2020-12-03T00-03-10Z</td>
        <td>"/usr/bin/docker-ent…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes (healthy)</td>
        <td>9000/tcp</td>
        <td>distributed_minio_1</td>
    </tr>
    <tr>
        <td>08b81e680c82</td>
        <td>quay.io/coreos/etcd:latest</td>
        <td>"etcd -listen-peer-u…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td>2379-2380/tcp</td>
        <td>distributed_etcd_1</td>
    </tr>
    <tr>
        <td>5622c872ed3e</td>
        <td>apachepulsar/pulsar:latest</td>
        <td>"bin/pulsar standalo…"</td>
        <td>7 minutes ago</td>
        <td>Up 7 minutes</td>
        <td></td>
        <td>distributed_pulsar_1</td>
    </tr>
</table>
</code>


> 运行 `$ sudo docker-compose down` 停止 Docker Compose。