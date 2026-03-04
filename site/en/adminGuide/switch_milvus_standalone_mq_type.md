---
id: switch_milvus_standalone_mq_type.md
summary: Learn how to switch the message queue type for Milvus standalone.
title: Switch MQ Type for Milvus Standalone
---

# Switch MQ Type for Milvus Standalone

This topic describes how to switch the message queue (MQ) type for an existing Milvus standalone deployment. Milvus supports online MQ switching without downtime.

<div class="alert warning">

This feature is pending release and is subject to change. Please reach out to Milvus support if you want to try it out or have any questions.

</div>

## Prerequisites

- A running Milvus Standalone instance installed via [Docker Compose](install_standalone-docker-compose.md).
- The Milvus instance has been upgraded to the latest version that supports this Switch MQ feature (v2.6.13 or later).

## General workflow

The general workflow for switching the MQ type is as follows:

1. Ensure the Milvus instance is running properly.
2. Confirm the source MQ type and the target MQ type.
3. Configure the target MQ's access settings into the Milvus configuration without changing the `mqType` value.
4. Trigger the switch by calling the WAL alter API.
5. Monitor the logs to verify the switch has completed successfully.

<div class="alert note">

Before switching, ensure that the target MQ does not contain topics with the same names as those used by the current Milvus instance.
This is especially important if the target MQ service has been previously used by another Milvus instance, as conflicting topic names can lead to unexpected behavior.

</div>

## Docker Compose Standalone: Switch from RocksMQ to Woodpecker (Local/MinIO)

This procedure applies to **Milvus Standalone Docker Compose** deployments that use RocksMQ by default.

### Step 1: Verify the Milvus instance is running

Ensure your Milvus Standalone docker compose instance is running properly. You can verify this by creating a test collection, inserting data, and running a query.

### Step 2: Configure Woodpecker with local storage

Update the Milvus configuration to add Woodpecker settings **without** changing the `mqType` value. Run `docker exec -it milvus-standalone bash` to enter the container, then edit the `/milvus/configs/user.yaml` file with the following key configuration:

```yaml
woodpecker:
  storage:
    type: minio   #  minio or local
```

Then restart the Milvus instance to apply the configuration:

```shell
docker-compose restart
```

### Step 3: Execute the MQ switch

<div class="alert note">

If you are switching to Woodpecker for the first time, you can skip this note. Otherwise, when switching repeatedly, make sure to clean up the related data before switching. Residual data may cause unexpected behavior. For example, switching from Woodpecker (MinIO/local) to RocksMQ and then back to Woodpecker requires cleaning up Woodpecker meta and data first.

</div>

Run the following command to trigger the switch to Woodpecker:

```shell
curl -X POST http://<mixcoord_addr>:<mixcoord_port>/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "woodpecker"}'
```

<div class="alert note">

This command sends a switch MQ type request to the internal MixCoord component in the standalone instance. Typically, the MixCoord port is `9091`.

</div>

### Step 4: Verify the switch is complete

The switch process completes automatically. Monitor the Milvus logs for the following key messages to confirm the switch has finished. Run the following command to check the switch progress:

```shell
docker logs milvus-standalone  | grep "successfully updated mq.type configuration in etcd"
```

If the switch is successful, the output should look similar to the following:

```
[INFO] [coordinator/wal_callbacks.go:90] ["successfully updated mq.type configuration in etcd"] [targetWALName=WoodPecker]
[config=null] [broadcastID=464677797180736841] [configKey=mq.type] [mqTypeValue=woodpecker]
```

### Step 5: [Optional] Clean up RocksMQ data

The RocksMQ data is located in the `volumes/milvus/rdb_data` and `volumes/milvus/rdb_data_meta_kv` directories defined in `docker-compose.yaml`.

<div class="alert note">

If you plan to switch back to RocksMQ in the future, you should clean up these data files first to avoid conflicts.

</div>

## Docker Compose Standalone: Switch from Woodpecker (Local/MinIO) to RocksMQ

This procedure applies to **Milvus Standalone Docker Compose** deployments that are currently using Woodpecker and want to switch to RocksMQ.

### Step 1: Verify the Milvus instance is running

Ensure your Milvus Standalone docker compose instance is running properly. You can verify this by creating a test collection, inserting data, and running a query.

### Step 2: Execute the MQ switch

<div class="alert note">

Ensure that the instance does not have residual RocksMQ data from a previous run. If this is your first time switching to RocksMQ, you can skip this note. Otherwise, clean up the related RocksMQ meta data and data first.

</div>

Run the following command to trigger the switch to RocksMQ:

```shell
curl -X POST http://<mixcoord_addr>:<mixcoord_port>/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "rocksmq"}'
```

<div class="alert note">

This command sends a switch MQ type request to the internal MixCoord component in the standalone instance. Typically, the MixCoord port is `9091`.

</div>

### Step 3: Verify the switch is complete

The switch process completes automatically. Monitor the Milvus logs for the following key messages to confirm the switch has finished. Run the following command to check the switch progress:

```shell
docker logs milvus-standalone  | grep "successfully updated mq.type configuration in etcd"
```

If the switch is successful, the output should look similar to the following:

```
[INFO] [coordinator/wal_callbacks.go:90] ["successfully updated mq.type configuration in etcd"] [targetWALName=rocksmq]
[config=null] [broadcastID=464677797180736841] [configKey=mq.type] [mqTypeValue=rocksmq]
```

### Step 4: [Optional] Clean up Woodpecker data

#### Clean up Woodpecker metadata

Use an etcd tool to delete the Woodpecker metadata. The key-value prefix is as follows:

- Prefix format: `<wp metadata rootPath>/...`
- Example: typically `woodpecker/...`

You can run the following command to view and then clean up the metadata:

```shell
etcdctl get woodpecker --prefix
```

#### Clean up Woodpecker storage data

If Woodpecker was using **MinIO mode**, delete the log data on object storage. Log in to MinIO and navigate to the corresponding bucket. The data path is as follows:

- Format: `<rootPath>/wp/<logId>/...`
- Example: typically `files/wp/...`

If Woodpecker was using **local mode**, the data is stored on the local disk at `volumes/milvus/data/wp/...`.

<div class="alert note">

If you plan to switch back to Woodpecker in the future, you should clean up these data files first to avoid conflicts.

</div>

## Supported MQ switch scenarios for Milvus Standalone

**Docker deployment (single container):** MQ switching is not supported because etcd source is not enabled and the `mq.type` config cannot be updated.

**Docker Compose deployment:**

| Source MQ | Target MQ | Status | Notes |
|-----------|-----------|--------|-------|
| RocksMQ | Woodpecker (MinIO/local) | **Supported** | |
| Woodpecker (MinIO/local) | RocksMQ | **Supported** | |
| Woodpecker MinIO | Woodpecker local | **Not supported** | Switching between Woodpecker storage modes requires additional metadata handling, which is not yet supported. May be supported in the future. |
| Woodpecker local | Woodpecker MinIO | **Not supported** | Same reason as above. |
| RocksMQ / Woodpecker (MinIO/local) | External Pulsar / Kafka | **Supported but not recommended** | Standalone instances should be kept as simple as possible for ease of operation and maintenance. |

<div class="alert note">

Avoid switching MQ types back and forth repeatedly. If you do need to switch, make sure to clean up the related data before each switch. Residual data may cause unexpected behavior.

</div>
