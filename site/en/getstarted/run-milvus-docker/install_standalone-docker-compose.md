---
id: install_standalone-docker-compose.md
label: Docker Compose
related_key: Docker Compose
summary: Learn how to install Milvus standalone with Docker Compose.
title: Run Milvus with Docker Compose (Linux)
---

# Run Milvus with Docker Compose (Linux)

This page illustrates how to launch a Milvus instance in Docker using Docker Compose.

## Prerequisites

- [Install Docker](https://docs.docker.com/get-docker/).
- Install the [Docker Compose plugin](https://docs.docker.com/compose/install/linux/) (V2 or later) and verify it with `docker compose version`. These instructions use `docker compose`, not the legacy `docker-compose` V1 command.
- [Check the requirements for hardware and software](prerequisite-docker.md) prior to your installation.

## Install Milvus

Milvus provides a Docker Compose configuration file in the Milvus repository. Download the configuration for v{{var.milvus_release_version}} and start a new deployment:

```shell
# Download the configuration file
$ wget https://github.com/milvus-io/milvus/releases/download/v{{var.milvus_release_version}}/milvus-standalone-docker-compose.yaml -O docker-compose.yaml

# Start Milvus
$ sudo docker compose up -d

Creating milvus-etcd  ... done
Creating milvus-minio ... done
Creating milvus-standalone ... done
```

<div class="alert note">

**Default deployment (v{{var.milvus_release_version}}):** `docker compose up -d` starts three long-running containers — `milvus-etcd` (metadata), `milvus-minio` (object storage), and `milvus-standalone`. The message queue is **Woodpecker (embedded, with MinIO / object storage as its WAL backend)**, so no separate message-queue container is required.

The configuration also runs the one-shot `milvus-volume-init` service to prepare data-directory ownership. It exits after completing that task.

**Message-queue default by version:**
- **2.5.x** — default message queue is **RocksMQ**.
- **2.6.x and later** — default message queue is **Woodpecker (embedded)**.

Use the configuration attached to the release you intend to install. For an existing deployment, follow the upgrade instructions instead of replacing its configuration with a new-installation file.

- If `docker compose` is unavailable, install the Compose plugin using the [Docker instructions](https://docs.docker.com/compose/install/linux/).

- If you encounter any issues pulling the image, contact us at <a href="mailto:community@zilliz.com">community@zilliz.com</a> with details about the problem, and we'll provide you with the necessary support.

</div>

After starting up Milvus,

- Containers named **milvus-standalone**, **milvus-minio**, and **milvus-etcd** are up.
  - The **milvus-etcd** container does not expose any ports to the host and maps its data to **volumes/etcd** in the current folder.
  - The **milvus-minio** container serves ports **9000** and **9001** locally with the default authentication credentials and maps its data to **volumes/minio** in the current folder.
  - The **milvus-standalone** container serves ports **19530** locally with the default settings and maps its data to **volumes/milvus** in the current folder.

You can check if the containers are up and running using the following command:

```shell
$ docker compose ps

NAME                IMAGE   COMMAND                  SERVICE      CREATED         STATUS                   PORTS
milvus-etcd         …       "etcd -advertise-cli…"   etcd         2 minutes ago   Up 2 minutes (healthy)   2379-2380/tcp
milvus-minio        …       "/usr/bin/docker-ent…"   minio        2 minutes ago   Up 2 minutes (healthy)   9000-9001/tcp
milvus-standalone   …       "/tini -- milvus run…"   standalone   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:9091->9091/tcp, 0.0.0.0:19530->19530/tcp
```

You can also access Milvus WebUI at `http://127.0.0.1:9091/webui/` to learn more about the your Milvus instance. For details, refer to [Milvus WebUI](milvus-webui.md).

To try the running server, follow the **Use an existing Milvus server** path in [Quickstart](quickstart.md) and connect to `http://localhost:19530`. Do not use the local `.db` connection block, which starts a separate Milvus Lite database.

## (Optional) Update Milvus configurations

To update Milvus configuration to suit your needs, you need to modify the `/milvus/configs/user.yaml` file within the `milvus-standalone` container.

1. Access the `milvus-standalone` container.

    ```shell
    docker exec -it milvus-standalone bash
    ```

1. Add extra configurations to override the default ones. 
  The following assumes that you need to override the default `proxy.healthCheckTimeout`. For applicable configuration items, refer to [System Configuration](system_configuration.md).

    ```shell
    cat << EOF > /milvus/configs/user.yaml
    # Extra config to override default milvus.yaml
    proxy:
      healthCheckTimeout: 1000 # ms, the interval that to do component healthy check
    EOF
    ```

1. Restart the `milvus-standalone` container to apply the changes.

    ```shell
    docker restart milvus-standalone
    ```

## Stop and delete Milvus

You can stop and delete this container as follows

```shell
# Stop Milvus
$ sudo docker compose down

# Delete service data
$ sudo rm -rf volumes
```

## Upgrade an existing deployment

For a Milvus 2.6.x standalone deployment, follow [Upgrade Milvus Standalone with Docker Compose](upgrade_milvus_standalone-docker.md). Back up metadata and persistent data, preserve the existing dependencies and configuration, and validate the documented source-to-target upgrade path before changing the Milvus image.

The 2.5.x-to-2.6.x message-queue instructions are not a procedure for upgrading directly to v{{var.milvus_release_version}}. Do not replace an older deployment's Compose file with the new-installation configuration above or change its message queue as part of an upgrade.

{{fragments/mq_upgrade_limitation.md}}

## Optional dependencies

This deployment runs **Woodpecker** (embedded, MinIO WAL backend) for messaging, **etcd** for metadata, and **MinIO** for object storage. To use a different message queue or connect external object storage / metadata, see:

- Message queue: [Woodpecker](woodpecker.md) (default) · [Pulsar](mq_pulsar.md) · [Kafka](mq_kafka.md) · [RocksMQ](mq_rocksmq.md)
- Object storage: [MinIO](deploy_s3.md) (default) · [AWS S3](deploy_s3.md) · [Azure Blob](abs.md) · [GCP Cloud Storage](gcs.md) · [Aliyun OSS](deploy_s3.md) · [Tencent COS](deploy_s3.md) · [Huawei OBS](deploy_s3.md) · [S3-compatible](deploy_s3.md)
- Metadata: [etcd](deploy_etcd.md)

{{fragments/storage_v3_installation_note.md}}

## What's next

Having installed Milvus in Docker, you can:

- Check [Quickstart](quickstart.md) to see what Milvus can do.

- Learn the basic operations of Milvus:
  - [Manage Databases](manage_databases.md)
  - [Manage Collections](manage-collections.md)
  - [Manage Partitions](manage-partitions.md)
  - [Insert, Upsert & Delete](insert-update-delete.md)
  - [Single-Vector Search](single-vector-search.md)
  - [Hybrid Search](multi-vector-search.md)

- [Upgrade Milvus Standalone with Docker Compose](upgrade_milvus_standalone-docker.md).
- [Scale your Milvus cluster](scaleout.md).
- Deploy your Milvus cluster on clouds:
  - [Amazon EKS](eks.md)
  - [Google Cloud](gcp.md)
  - [Microsoft Azure](azure.md)
- Explore [Milvus WebUI](milvus-webui.md), an intuitive web interface for Milvus observability and management.
- Explore [Milvus Backup](milvus_backup_overview.md), an open-source tool for Milvus data backups.
- Explore [Birdwatcher](birdwatcher_overview.md), an open-source tool for debugging Milvus and dynamic configuration updates.
- Explore [Attu](https://github.com/zilliztech/attu), an open-source GUI tool for intuitive Milvus management.
- [Monitor Milvus with Prometheus](monitor.md).
