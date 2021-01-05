---
id: compatibility_information.md
title: 版本兼容性说明
sidebar_label: 版本兼容性说明
---

# 版本兼容性说明

本版已不再维护。建议将数据迁移至 v0.10.x。本文以迁移至 v0.10.3 为例。

<div class="alert warning">
本版本与 v0.11.0 <b>不</b>兼容。
</div>

## 第 1 步：产生待迁移数据

<details>
<summary><font color="#4fc4f9">如已有旧版本数据，可以略过此步骤。</font></summary> 

1. 在本地创建一个 <b>milvus</b> 文件夹，作为 Milvus 的运行目录： 

    <code>
    cd ~ 
    mkdir milvus 
    cd milvus 
    </code>

2. 新建一个 <b>conf</b> 目录存放 Milvus 配置文件： 

    <code>
    mkdir conf 
    cd conf 
    </code>

3. 下载当前版本 Milvus 的配置文件： 

    <code>
    wget https://raw.githubusercontent.com/milvus-io/milvus/{{var.release_version}}/core/conf/demo/server_config.yaml 
    wget https://raw.githubusercontent.com/milvus-io/milvus/{{var.release_version}}/core/conf/demo/log_config.conf 
    </code>
    
    <div class="alert note">
    如果下载不成功，可在网页中打开下载网址，在 conf 目录下新建同名文件，把网页中的内容粘贴到文件中保存。
    </div> 

4. 启动一个 CPU 版 Milvus 的容器，将 Milvus 运行路径映射到刚才创建的 milvus 目录： 

    <code>
    docker pull milvusdb/milvus:{{var.cpu_milvus_docker_image_version}}
    docker run -it -d -p 19530:19530 -v ~/milvus/db:/var/lib/milvus/db -v ~/milvus/conf:/var/lib/milvus/conf -v ~/milvus/logs:/var/lib/milvus/logs -v ~/milvus/wal:/var/lib/milvus/wal milvusdb/milvus:{{var.cpu_milvus_docker_image_version}}
    </code>

5. 安装与当前 Milvus 版本对应的 Python SDK：
    
    <code>
    pip3 install pymilvus=={{var.milvus_python_sdk_version}}
    </code>

6. 创建一个名为 TEST 的集合，在该集合下创建两个分区，插入数万条数据并建立索引。 

完成后，milvus 文件夹下的结构如下图所示 ：

<img src="../../../assets/assets/milvus_sudo_tree.png">

</details>

## 第 2 步：关闭当前版本 Milvus

1. 停止当前版本的 Milvus。

    ```
    docker stop [Your_milvus_container_id]
    ```

2. 删除 **/milvus** 下的 **/conf**、**/logs** 和 **/wal** 文件夹：

    ```
    cd ~/milvus
    sudo rm -rf ./conf
    sudo rm -rf ./logs
    sudo rm -rf ./wal
    ```
    <div class="alert note">
    如需保留日志文件，请将 logs 文件夹备份到其他目录。
    </div>

## 第 3 步：下载配置文件

新建 conf 目录并下载 v0.10.3 的配置文件：

```
mkdir conf
cd conf
wget https://raw.githubusercontent.com/milvus-io/milvus/0.10.3/core/conf/demo/server_config.yaml
```

## 第 4 步：确认、更新 MySQL/SQLite 服务端地址

```
vim ./server_config.yaml
```

确保新版本配置项 `general.meta_uri` 指定的 MySQL/SQLite 服务端地址与老版本配置项 `db_config.backend_url` 指定的服务端地址一致。以 MySQL 为例，更新的配置信息如下所示：

```
 general:
  timezone:UTC+8
  meta_uri: mysql://root:123456@<MySQL_server_host IP>:3306/milvus
```

### 第 5 步：下载并启动新版 Milvus

使用相同的映射路径下载并启动 v0.10.3 Milvus 容器：

```
docker pull milvusdb/milvus:0.10.3-cpu-d091720-f962e8
docker run -it -d -p 19530:19530 -v ~/milvus/db:/var/lib/milvus/db -v ~/milvus/conf:/var/lib/milvus/conf -v ~/milvus/logs:/var/lib/milvus/logs -v ~/milvus/wal:/var/lib/milvus/wal milvusdb/milvus:0.10.3-cpu-d091720-f962e8
```

### 第 6 步：安装对应版本的 Python SDK

```
pip3 install pymilvus==0.2.14
```

### 第 7 步：验证数据正确性

1. 编写 Python 脚本调用相关接口验证数据正确性：

    编写一个验证数据正确性的 Python 脚本并运行，例如：

    ```
    from milvus import Milvus

    COLLECTION_NAME = "TEST"
    MILVUS = Milvus(host="127.0.0.1", port="19530")
    status, info = MILVUS.get_collection_info(collection_name=COLLECTION_NAME)
    print(info)
    status, row_count = MILVUS.count_entities(collection_name=COLLECTION_NAME)
    print(COLLECTION_NAME, "row count =", row_count)
    status, index = MILVUS.get_index_info(collection_name=COLLECTION_NAME)
    print('Index:', index)
    stat, collections = MILVUS.list_collections()
    print('Collections:', collections)
    stat, partitions = MILVUS.list_partitions(collection_name=COLLECTION_NAME)
    print('Partitions:', partitions)
    ```
     
2. 脚本运行后，检查返回信息是否与原始数据一致。

    <div class="alert note">
    以下示例显示的信息与第 1 步所创建的待迁移数据一致。
    </div>

    ```
    CollectionSchema(collection_name='TEST', dimension=256, index_file_size=1024, metric_type=<MetricType: L2>)
    TEST row count = 60000
    Index: (collection_name='TEST', index_type=<IndexType: IVFLAT>, params={'nlist': 4096})
    Collections: ['TEST']
    Partitions: [(collection_name='TEST', tag='_default'), (collection_name='TEST', tag='part_0'), (collection_name='TEST', tag='part_1')]
    ```
