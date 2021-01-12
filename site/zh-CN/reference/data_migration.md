---
id: data_migration.md
---

# 迁移数据至 Milvus v{{var.release_version}}

本文介绍如何从 Milvus v0.7.x/0.8.x/0.9.x/0.10.x 迁移至 Milvus v{{var.release_version}}。

<div class="alert warning">
本版本与 v0.11.0 <b>不兼容</b>。
</div>

### 第 1 步：关闭当前版本 Milvus

1. 停止当前版本的 Milvus：

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
    如需保留日志文件，请将 <b>logs</b> 文件夹备份到其他目录。
    </div>

### 第 2 步：下载配置文件

新建 **conf** 目录并下载 Milvus v{{var.release_version}} 的配置文件：

```
mkdir conf
cd conf
wget https://raw.githubusercontent.com/milvus-io/milvus/{{var.release_version}}/core/conf/demo/server_config.yaml
```

<div class="alert note">
如果下载不成功，可在网页中打开下载网址，在 <b>conf</b> 目录下新建同名文件，把网页中的内容粘贴到文件中保存。 
</div>

### 第 3 步：确认、更新 MySQL/SQLite 服务端地址

```
vim ./server_config.yaml
```

确保新版本配置项 `general.meta_uri` 指定的 MySQL/SQLite 服务端地址与老版本配置项 `db_config.backend_url` 指定的服务端地址一致。以 MySQL 为例，更新的配置信息如下所示：

```
 general:
  timezone:UTC+8
  meta_uri: mysql://root:123456@<MySQL_server_host IP>:3306/milvus
```

### 第 4 步：下载并启动 Milvus v{{var.release_version}}

使用与当前版本相同的映射路径下载并启动 Milvus v{{var.release_version}} 容器：

```
docker pull milvusdb/milvus:{{var.cpu_milvus_docker_image_version}}
docker run -it -d -p 19530:19530 -v ~/milvus/db:/var/lib/milvus/db -v ~/milvus/conf:/var/lib/milvus/conf -v ~/milvus/logs:/var/lib/milvus/logs -v ~/milvus/wal:/var/lib/milvus/wal milvusdb/milvus:{{var.cpu_milvus_docker_image_version}}
```

### 第 5 步：安装对应版本的 Python SDK

```
pip3 install pymilvus=={{var.milvus_python_sdk_version}}
```

### 第 6 步：验证数据正确性

编写 Python 脚本调用相关接口验证数据正确性。