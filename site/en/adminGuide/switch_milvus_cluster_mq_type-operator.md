---
id: switch_milvus_cluster_mq_type-operator.md
summary: Learn how to switch the message queue type for a Milvus cluster.
title: Switch MQ Type for Milvus Cluster
---

# Switch MQ Type for Milvus Cluster

This topic describes how to switch the message queue (MQ) type for an existing Milvus cluster deployment. Milvus supports online MQ switching between Pulsar, Kafka, and Woodpecker without downtime.

<div class="alert warning">

This feature is pending release and is subject to change. Please reach out to Milvus support if you want to try it out or have any questions.

</div>

## Prerequisites

- A running Milvus cluster instance installed via [Milvus Operator](install_cluster-milvusoperator.md).
- The Milvus instance has been upgraded to the latest version that supports this Switch MQ feature (v2.6.14 or later).

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

However, Milvus Operator currently does not expose the MixCoord service. You need to use `kubectl exec` to enter the MixCoord pod and run the `curl` command from inside the pod.

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

### Step 4: Update the MQ type in the Operator ConfigMap

Update the MQ type in the Operator ConfigMap to Woodpecker. First, create a file named `change_configmap.yaml`:

```yaml
apiVersion: milvus.io/v1beta1
kind: Milvus
metadata:
  name: my-release
  labels:
    app: milvus
spec:
  dependencies:
    msgStreamType: woodpecker
```

Then apply the configuration update:

```shell
kubectl patch -f change_configmap.yaml --patch-file change_configmap.yaml --type merge
```

### Step 5: [Optional] Stop Pulsar pods and clean up Pulsar data

#### For builtin Pulsar instances

After confirming the switch to Woodpecker is successful, you can remove the Pulsar pods and their associated PVC data.

Run the following command to uninstall Pulsar:

```shell
helm uninstall my-release-pulsar
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

This is currently not supported. When Milvus Operator sets the MQ type to Woodpecker, it does not allow pre-configuring the Pulsar/Kafka connection address in the configuration file, which is required for the switch.

## Supported MQ switch scenarios for Operator-installed Milvus Cluster

| Source MQ | Target MQ | Status | Notes                                                                                                                    |
|-----------|-----------|--------|--------------------------------------------------------------------------------------------------------------------------|
| Builtin Pulsar | Woodpecker (MinIO) | **Supported** |                                                                                                                          |
| Builtin Pulsar | External Kafka | **Not supported** | Milvus Operator does not support pre-configuring the Kafka access address.                                               |
| Builtin Pulsar | Builtin Kafka | **Not supported** | Helm does not support installing two builtin MQ systems simultaneously.                                                  |
| External Pulsar | Woodpecker (MinIO) | **Supported** |                                                                                                                          |
| External Pulsar | External Kafka | **Not supported** | Milvus Operator does not support pre-configuring the Kafka access address.                                               |
| Builtin Kafka | Woodpecker (MinIO) | **Supported** |                                                                                                                          |
| Builtin Kafka | External Pulsar | **Not supported** | Milvus Operator does not support pre-configuring the Pulsar access address.                                              |
| Builtin Kafka | Builtin Pulsar | **Not supported** | Helm does not support installing two builtin MQ systems simultaneously.                                                  |
| External Kafka | Woodpecker (MinIO) | **Supported** |                                                                                                                          |
| External Kafka | External Pulsar | **Not supported** | Milvus Operator does not support pre-configuring the Pulsar access address.                                              |
| Builtin/external Pulsar/Kafka | Woodpecker (local) | **Supported but not recommended** | All pods must access the same local disk (e.g., NFS mount), and additional configuration is required.                    |
| Woodpecker local | Woodpecker MinIO | **Not supported** | Switching between Woodpecker storage modes is not yet supported. May be supported in the future, but not recommended because Woodpecker local mode should not be used in cluster deployments. |

<div class="alert note">

Avoid switching MQ types back and forth repeatedly. If you do need to switch, make sure to clean up the related data before each switch. Residual data may cause unexpected behavior.

</div>
