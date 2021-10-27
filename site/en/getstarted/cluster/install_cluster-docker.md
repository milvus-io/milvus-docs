---
id: install_cluster-docker.md
label: Install with Docker Compose
order: 0
group: cluster
summary: Installation instructions for the cluster version of Milvus.

---

# Install Milvus Cluster

{{fragments/installation_guide_cluster.md}}

{{tab}}


## Download an installation file

[Download **milvus-cluster-docker-compose.yml**](https://github.com/milvus-io/milvus/releases/download/v{{var.cpu_milvus_docker_image_version}}/milvus-cluster-docker-compose.yml) directly or with the following command, and save it as **docker-compose.yml**.

```
$ wget https://github.com/milvus-io/milvus/releases/download/v{{var.cpu_milvus_docker_image_version}}/milvus-cluster-docker-compose.yml -O docker-compose.yml
```

## Configure Milvus (optional)

[Download **milvus.yaml**](https://raw.githubusercontent.com/milvus-io/milvus/v{{var.cpu_milvus_docker_image_version}}/configs/milvus.yaml) directly or with the following command, and modify the configurations to suit your needs. See [Milvus Cluster System Configurations](configuration_cluster-basic.md) for more information.

```
$ wget https://raw.githubusercontent.com/milvus-io/milvus/v{{var.cpu_milvus_docker_image_version}}/configs/milvus.yaml
```

In **docker-compose.yml**, add a `volumes` section under each Milvus component, i.e. root coord, data coord, data node, query coord, query node, index coord, index node, and proxy. And map the local path to your **milvus.yaml** file onto the corresponding docker container paths to the configuration files **/milvus/configs/milvus.yaml** under all `volumes` sections.

```yaml
...
proxy:
    container_name: milvus-proxy
    image: milvusdb/milvus:v2.0.0-rc7-20211011-d567b21
    command: ["milvus", "run", "proxy"]
    volumes:       # Add a volumes section.
      - /local/path/to/your/file:/milvus/configs/milvus.yaml   # Map the local path to the container path
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
      PULSAR_ADDRESS: pulsar://pulsar:6650
    ports:
      - "19530:19530"
...
```

<div class="alert note">
Data is stored in the <b>volumes</b> folder according to the default configuration in <b>docker-compose.yml</b>. To change the folder to store data, edit <b>docker-compose.yml</b> or run <code>$ export DOCKER_VOLUME_DIRECTORY=</code>.
</div>

## Start Milvus

```Shell
$ docker-compose up -d
```

```Text
Docker Compose is now in the Docker CLI, try `docker compose up`
Creating milvus-etcd   ... done
Creating milvus-minio  ... done
Creating milvus-pulsar ... done
Creating milvus-proxy      ... done
Creating milvus-rootcoord  ... done
Creating milvus-indexcoord ... done
Creating milvus-querycoord ... done
Creating milvus-datacoord  ... done
Creating milvus-querynode  ... done
Creating milvus-indexnode  ... done
Creating milvus-datanode   ... done
```

*After Milvus cluster starts, 11 running docker containers appear including three infrastructure services and eight Milvus services.*

```
$ sudo docker ps
```
```
      Name                     Command                  State                          Ports
----------------------------------------------------------------------------------------------------------------
milvus-datacoord    /tini -- milvus run datacoord    Up
milvus-datanode     /tini -- milvus run datanode     Up
milvus-etcd         etcd -listen-peer-urls=htt ...   Up (healthy)   2379/tcp, 2380/tcp
milvus-indexcoord   /tini -- milvus run indexcoord   Up
milvus-indexnode    /tini -- milvus run indexnode    Up
milvus-minio        /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp
milvus-proxy        /tini -- milvus run proxy        Up             0.0.0.0:19530->19530/tcp,:::19530->19530/tcp
milvus-pulsar       bin/pulsar standalone            Up
milvus-querycoord   /tini -- milvus run querycoord   Up
milvus-querynode    /tini -- milvus run querynode    Up
milvus-rootcoord    /tini -- milvus run rootcoord    Up
```

## Stop Milvus

To stop Milvus cluster, run <code> $ sudo docker-compose down</code>.

To delete data after stopping Milvus, run <code> $ sudo rm -rf  volumes</code>.

## What's next

Having installed Milvus, You can:

- Check [Hello Milvus](example_code.md) to run an example code with different SDKs to see what Milvus can do.

- Learn the basic operations of Milvus:
  - [Connect to Milvus server](connect.md)
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)

- [Upgrade Milvus Using Helm Chart](upgrade.md).
- Explore [MilvusDM](migrate_overview.md), an open-source tool designed for importing and exporting data in Milvus.
- [Monitor Milvus with Prometheus](monitor.md).
