---
id: install_standalone-docker.md
title: Install Milvus Standalone
label: Install with Docker
order: 0
group: standalone
---

# Install Milvus Standalone

## Before You Begin<a href="#cpu_support"></a>

Before moving forward to installation, you must check the eligibility of your Docker, Docker Compose, and hardware in line with Milvus' requirement.

<details><summary>Check your Docker and Docker Compose version</summary>

<div class="alert note">
Docker Compose is the recommended way to install Milvus.
</div>

<li>Docker version 19.03 or higher is required. </li>
<li>Docker Compose version 1.25.1 or higher is required. </li>
</details>
<details><summary>Check whether your CPU supports SIMD extension instruction set</summary>

{{fragments/cpu_support.md}}
</details>

<details><summary>Check your GPU’s eligibility</summary>
Milvus Standalone supports GPU acceleration on floating vectors. 
{{fragments/gpu_support.md}}
</details>

## Install Milvus Standalone

{{tab}}

1. Check Docker version:

```
$ sudo docker info
```

> Follow [Get Docker](https://docs.docker.com/get-docker/) to install Docker on your system.

2. Check Docker Compose version:

```
$ sudo docker-compose version
```

> See [Install Docker Compose](https://docs.docker.com/compose/install/) for Docker Compose installation guide.

3. Pull the Docker image:

```
$ sudo docker pull milvusdb/milvus:2.0.0-d043021-19c36b
```

4. Download **docker-compose.standalone.yml** and save it as **docker-compose.yml**:

```
$ mkdir -p /home/$USER/milvus
$ cd home/$USER/milvus
$ wget https://raw.githubusercontent.com/milvus-io/milvus/v2.0.0/deployments/docker/docker-compose.standalone.yml -O docker-compose.yml
$ wget https://raw.githubusercontent.com/milvus-io/milvus/v2.0.0/deployments/docker/.env
```
> The **.env** file contains all variable definitions used in **docker-compose.yml**. Ensure that you set the docker image in `TARGET_DOCKER_IMAGE` to the image defined in the **.env** file.
```
TARGET_DOCKER_IMAGE=milvusdb/milvus:2.0.0-d
```



| Variable      | Definition |
| ----------- | ----------- |
| TARGET_DOCKER_IMAGE         | Docker image.       |
| ETCD_ADDRESS   | 	Etcd service address.        |
| MINIO_ADDRESS      | MinIO service address.       |
| MASTER_ADDRESS   | Master service address.        |
| PROXY_SERVICE_ADDRESS      | Proxy service address.       |
| INDEX_SERVICE_ADDRESS   | Index service address.        |
| DATA_SERVICE_ADDRESS      | Data service address.       |
| QUERY_SERVICE_ADDRESS   | Query service address.        |

<br/>

5. Start Docker Compose.

```
$ sudo docker-compose up -d 
```
*If Docker Compose boots successfully, three running docker containers will appear (two infrastructure services and one Milvus service):*

<code>
$ docker ps 
<table>
    <tr>
        <td>CONTAINER ID</td>
        <td>Image</td>
        <td>Command</td>
        <td>Created</td>
        <td>Status</td>
        <td>Ports</td>
        <td>Names</td>
    </tr>
    <tr>
        <td>3baf500700ff</td>
        <td>milvusdb/milvus:2.0.0-d043021-19c36b</td>
        <td>"/tini -- /milvus-di…"</td>
        <td>3 seconds ago</td>
        <td>6 seconds ago</td>
        <td>0.0.0.0:19530-&gt;19530/tcp</td>
        <td>deploy_standalone_1</td>
    </tr>
    <tr>
        <td>d807e1e1e9b1</td>
        <td>quay.io/coreos/etcd:latest</td>
        <td>"etcd -listen-peer-u…"</td>
        <td>6 seconds ago</td>
        <td>Up 4 seconds</td>
        <td>0.0.0.0:2379-2380-&gt;2379-2380/tcp, 0.0.0.0:4001-&gt;4001/tcp</td>
        <td>deploy_etcd_1</td>
    </tr>
    <tr>
        <td>a103514a959a</td>
        <td>minio/minio:RELEASE.2020-12-03T00-03-10Z</td>
        <td>"/usr/bin/docker-ent…"</td>
        <td>6 seconds ago</td>
        <td>Up 4 seconds (health: starting)</td>
        <td>0.0.0.0:9000-&gt;9000/tcp</td>
        <td>deploy_etcd_1</td>
    </tr>
</table>
</code>

> To stop Docker Compose, run ```$ sudo docker-compose down```.