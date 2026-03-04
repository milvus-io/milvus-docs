---
id: switch_milvus_cluster_mq_type-helm.md
summary: Learn how to switch the message queue type for a Milvus cluster.
title: Switch MQ Type for Milvus Cluster
---

# Switch MQ Type for Milvus Cluster

This topic describes how to switch the message queue (MQ) type for an existing Milvus cluster deployment. Milvus supports online MQ switching between Pulsar, Kafka, and Woodpecker without downtime.

<div class="alert warning">

This feature is pending release and is subject to change. Please reach out to Milvus support if you want to try it out or have any questions.

</div>

## Prerequisites

- A running Milvus cluster instance installed via [Helm](install_cluster-helm.md).
- The Milvus instance has been upgraded to the latest version that supports this Switch MQ feature (v2.6.13 or later).

## Switch from builtin/external Pulsar/Kafka to Woodpecker (MinIO)

Follow these steps to switch the MQ type from Pulsar or Kafka to Woodpecker with MinIO storage.

### Step 1: Verify the Milvus instance is running

Before switching, ensure that your Milvus cluster instance is running properly. You can verify this by creating a test collection, inserting data, and running a query.

### Step 2: Execute the MQ switch

<div class="alert note">

If you are switching to Woodpecker for the first time, you can skip this note. Otherwise, when switching repeatedly, make sure to clean up the related data before switching. Residual data may cause unexpected behavior. For example, switching from Woodpecker (MinIO/local) to another MQ and then back to Woodpecker requires cleaning up Woodpecker meta and data first.

</div>

Run the following command to trigger the switch to Woodpecker:

```shell
curl -X POST http://<mixcoord_addr>:<mixcoord_port>/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "woodpecker"}'
```

<div class="alert note">

Replace `<mixcoord_addr>` and `<mixcoord_port>` with the actual address of your MixCoord service. You can typically use `kubectl port-forward` to expose the MixCoord management interface:

```shell
kubectl port-forward --address 0.0.0.0 service/my-release-milvus-mixcoord 29091:9091
```

In this case, `mixcoord_addr` is the IP of the machine running the command, and `mixcoord_port` is the forwarded port `29091`.

</div>

### Step 3: Verify the switch is complete

The switch process completes automatically. Monitor the Milvus logs for the following key messages to confirm the switch has finished:

```shell
kubectl logs my-release-milvus-mixcoord-68d9889549-vdj8n  | grep "successfully updated mq.type configuration in etcd"
```

If the switch is successful, the output should look similar to the following:

```
[INFO] [coordinator/wal_callbacks.go:90] ["successfully updated mq.type configuration in etcd"]
[targetWALName=WoodPecker] [config=null] [broadcastID=464632819924869973] [configKey=mq.type] [mqTypeValue=woodpecker]
```

### Step 4: [Optional] Stop Pulsar pods and clean up Pulsar data

#### For builtin Pulsar instances

After confirming the switch to Woodpecker is successful, you can remove the Pulsar pods and their associated PVC data.

Run the following command to disable Pulsar and enable Woodpecker:

```shell
helm upgrade my-release zilliztech/milvus \
  --set image.all.tag=v2.6.13 \
  --set pulsarv3.enabled=false \
  --set woodpecker.enabled=true \
  --set streaming.enabled=true \
  --set indexNode.enabled=false
```

Run the following commands to delete the Pulsar PVC storage:

```shell
# Delete Pulsar bookie journal PVCs
kubectl delete pvc my-release-pulsarv3-bookie-journal-my-release-pulsarv3-bookie-0
kubectl delete pvc my-release-pulsarv3-bookie-journal-my-release-pulsarv3-bookie-1
kubectl delete pvc my-release-pulsarv3-bookie-journal-my-release-pulsarv3-bookie-2

# Delete Pulsar bookie ledger PVCs
kubectl delete pvc my-release-pulsarv3-bookie-ledgers-my-release-pulsarv3-bookie-0
kubectl delete pvc my-release-pulsarv3-bookie-ledgers-my-release-pulsarv3-bookie-1
kubectl delete pvc my-release-pulsarv3-bookie-ledgers-my-release-pulsarv3-bookie-2

# Delete Pulsar ZooKeeper PVCs
kubectl delete pvc my-release-pulsarv3-zookeeper-data-my-release-pulsarv3-zookeeper-0
kubectl delete pvc my-release-pulsarv3-zookeeper-data-my-release-pulsarv3-zookeeper-1
kubectl delete pvc my-release-pulsarv3-zookeeper-data-my-release-pulsarv3-zookeeper-2
```

<div class="alert note">

If you plan to switch back to Pulsar in the future, you should clean up these data files first to avoid conflicts. Currently, due to Helm chart limitations, it is not possible to switch back to a builtin Pulsar instance.

</div>

#### For external Pulsar instances

You can clean up the Milvus-related topics in the external Pulsar instance. The Milvus topic naming format is:

```
<cluster_prefix>-dml_<seqNo>_<TimeTick><Version>
```

For example: `by-dev-rootcoord-dml_10_464633776992639586v0`

<div class="alert note">

If you plan to switch back to external Pulsar in the future, you should clean up these topics first to avoid conflicts.

</div>

## Switch from Woodpecker (MinIO) to external Pulsar/Kafka

Follow these steps to switch the MQ type from Woodpecker back to external Pulsar or external Kafka.

### Step 1: Verify the Milvus instance is running

Before switching, ensure that your Milvus cluster instance is running properly.

### Step 2: Configure the target MQ connection configuration

Before triggering the switch, you need to ensure the target MQ service (Pulsar or Kafka) is available and its access configuration is rendered into the Milvus configuration.

<div class="alert note">

The exact steps in this section depend on whether you are using an internal (bundled) or external MQ service.

</div>

If you are using the bundled Pulsar or Kafka deployed by Helm, update your Helm release to enable the target MQ service and disable Woodpecker.
The `streaming.enabled=true` flag is required to enable the Streaming Node, which is a prerequisite for the Switch MQ feature. For example, to switch to Pulsar:

First, create or edit a `values.yaml` file:

```yaml
extraConfigFiles:
  user.yaml: |+
    pulsar:
      address: <pulsar addr>
      port: <pulsar port, e.g. 6650>
```

```shell
helm upgrade -i my-release milvus/milvus \
  --set pulsarv3.enabled=true \
  --set woodpecker.enabled=false \
  --set streaming.enabled=true \
  -f values.yaml
```

After the upgrade, wait for all pods to be ready. Then, verify that the target MQ access configuration has been rendered into the Milvus configuration.

### Step 3: Execute the MQ switch

<div class="alert note">

Ensure that the target Pulsar/Kafka does not contain Milvus topics from a previous configuration. If this is your first time switching to Pulsar, you can skip this note. Otherwise, clean up the residual Milvus topics with the same names in Pulsar/Kafka first.

</div>

Run the following command to trigger the switch to Pulsar (replace `pulsar` with `kafka` if switching to Kafka):

```shell
curl -X POST http://<mixcoord_addr>:<mixcoord_port>/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "pulsar"}'
```

<div class="alert note">

Replace `<mixcoord_addr>` and `<mixcoord_port>` with the actual address of your MixCoord service. You can typically use `kubectl port-forward` to expose the MixCoord management interface:

```shell
kubectl port-forward --address 0.0.0.0 service/my-release-milvus-mixcoord 29091:9091
```

In this case, `mixcoord_addr` is the IP of the machine running the command, and `mixcoord_port` is the forwarded port `29091`.

</div>

### Step 4: Verify the switch is complete

The switch process completes automatically. Monitor the Milvus logs for the following key messages to confirm the switch has finished:

```shell
kubectl logs my-release-milvus-mixcoord-68d9889549-vdj8n  | grep "successfully updated mq.type configuration in etcd"
```

If the switch is successful, the output should look similar to the following:

```
[INFO] [coordinator/wal_callbacks.go:90] ["successfully updated mq.type configuration in etcd"]
[targetWALName=pulsar] [config=null] [broadcastID=464632819924869973] [configKey=mq.type] [mqTypeValue=pulsar]
```

### Step 5: [Optional] Clean up Woodpecker data on MinIO/S3 and etcd

Log in to MinIO/S3 and navigate to the corresponding bucket. Delete the Woodpecker data at the following path:

- Format: `<rootPath>/wp/<logId>/...`
- Example: typically `files/wp/...`

Use an etcd tool to delete the Woodpecker metadata. The key-value prefix is as follows:

- Prefix format: `<wp metadata rootPath>/...`
- Example: typically `woodpecker/...`

You can run the following command to view and then clean up the metadata:

```shell
etcdctl get woodpecker --prefix
```

<div class="alert note">

If you plan to switch back to Woodpecker in the future, you should clean up these data files first to avoid conflicts.

</div>

## Supported MQ switch scenarios for Helm-installed Milvus Cluster

| Source MQ | Target MQ | Status | Notes |
|-----------|-----------|--------|-------|
| Builtin Pulsar | Woodpecker (MinIO) | **Supported** | |
| Builtin Pulsar | External Kafka | **Supported** | |
| Builtin Pulsar | Builtin Kafka | **Not supported** | Helm does not support installing two builtin MQ systems simultaneously. |
| External Pulsar | Woodpecker (MinIO) | **Supported** | |
| External Pulsar | External Kafka | **Supported** | |
| Builtin Kafka | Woodpecker (MinIO) | **Supported** | |
| Builtin Kafka | External Pulsar | **Supported** | |
| Builtin Kafka | Builtin Pulsar | **Not supported** | Helm does not support installing two builtin MQ systems simultaneously. |
| External Kafka | Woodpecker (MinIO) | **Supported** | |
| External Kafka | External Pulsar | **Supported** | |
| Builtin/external Pulsar/Kafka | Woodpecker (local) | **Supported but not recommended** | All pods must access the same local disk (e.g., NFS mount), and additional configuration is required. |
| Woodpecker local | Woodpecker MinIO | **Not supported** | Switching between Woodpecker storage modes is not yet supported. May be supported in the future, but not recommended because Woodpecker local mode should not be used in cluster deployments. |

<div class="alert note">

Avoid switching MQ types back and forth repeatedly. If you do need to switch, make sure to clean up the related data before each switch. Residual data may cause unexpected behavior.

</div>
