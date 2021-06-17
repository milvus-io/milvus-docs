---
id: install_cluster-docker.md
title: Install Milvus Cluster
label: Install with Docker
order: 0
group: cluster
---

# Install Milvus Cluster

## Before You Begin

Before moving forward to installation, you must check the eligibility of your hardware in line with Milvus' requirement.

<details><summary>Check your Docker and Docker Compose version</summary>

<div class="alert note">
Docker Compose is the recommended way to install Milvus.
</div>

- Docker version 19.03 or higher is required.
- Docker Compose version 1.25.1 or higher is required. 
</details>

<details><summary>Check whether your CPU supports SIMD extension instruction set</summary>

{{fragments/cpu_support.md}}
</details>

<details><summary>Check your GPU’s eligibility</summary>
Milvus Cluster supports GPU acceleration on floating vectors. 
{{fragments/gpu_support.md}}
</details>

## Install Milvus Cluster

{{tab}}

1. Docker version 19.03 or higher is required. Check Docker version:

```
$ sudo docker info
```

> Follow [Get Docker](https://docs.docker.com/get-docker/) to install Docker on your system.

2. Docker Compose version 1.25.1 or higher is required. Check Docker Compose version:

```
$ sudo docker-compose version
```

> See [Install Docker Compose](https://docs.docker.com/compose/install/) for Docker Compose installation guide.

3. Download **docker-compose.yml**.

```
$ mkdir -p /home/$USER/milvus
$ cd home/$USER/milvus
$ wget https://raw.githubusercontent.com/milvus-io/milvus/v2.0.0/deployments/docker/distributed/docker-compose.yml
```
4. Start Docker Compose.
```
$ sudo docker-compose up -d 
```

*If Docker Compose boots successfully, 12 running docker containers will appear (nine infrastructure services and three Milvus services):*

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

> To stop Docker Compose, run ```$ sudo docker-compose down```.