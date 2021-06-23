---
id: install_standalone-docker.md
title: Install Milvus Standalone
label: Install with Docker Compose
order: 0
group: standalone
---

# Install Milvus Standalone
You can install Milvus Standalone with Docker Compose or Helm.

{{tab}}

## Before You Begin

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


1. Pull the Docker image:

```
$ sudo docker pull milvusdb/milvus:2.0.0-d043021-19c36b
```

2. Download **docker-compose.standalone.yml** and save it as **docker-compose.yml**:

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

3. Start Docker Compose.

```
$ sudo docker-compose up -d 
```
*If Docker Compose boots successfully, three running docker containers will appear (two infrastructure services and one Milvus service):*

```
$ docker ps 
```

> To stop Docker Compose, run ```$ sudo docker-compose down```.
