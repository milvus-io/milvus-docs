---
id: switch-kafka-woodpecker.md
title: Switch between Kafka and Woodpecker
summary: Switch the message queue of a Milvus cluster between Kafka and Woodpecker, with Helm or Milvus Operator.
---

# Switch between Kafka and Woodpecker

This page describes how to switch the message queue (MQ) of a **Milvus cluster** between **Kafka** (builtin or external) and **Woodpecker** (MinIO backend), in both directions, for Helm and Milvus Operator deployments. For the general workflow and prerequisites, see [Switch MQ Type](switch-mq-type.md).

## Switch from Kafka to Woodpecker

### Step 1: Verify the Milvus instance is running

Before switching, ensure your Milvus cluster is running properly — for example, by creating a test collection, inserting data, and running a query.

### Step 2: Execute the MQ switch

```shell
curl -X POST http://<mixcoord_addr>:<mixcoord_port>/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "woodpecker"}'
```

<div class="alert note">

Expose the MixCoord management interface to reach it:

- **Helm:** use `kubectl port-forward --address 0.0.0.0 service/my-release-milvus-mixcoord 29091:9091`; then `mixcoord_addr` is the machine's IP and `mixcoord_port` is `29091`.
- **Milvus Operator:** the MixCoord service is not exposed — use `kubectl exec` into the MixCoord pod and run the `curl` command from inside the pod.

</div>

### Step 3: Verify the switch is complete

```shell
kubectl logs <mixcoord-pod>  | grep "successfully updated mq.type configuration in etcd"
```

A successful switch logs `[mqTypeValue=woodpecker]`.

### Step 4 (Milvus Operator only): Update the MQ type in the Operator

Update the MQ type in the Operator-managed configuration. Create `change_configmap.yaml`:

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

```shell
kubectl patch -f change_configmap.yaml --patch-file change_configmap.yaml --type merge
```

### Step 5: (Optional) Stop Kafka and clean up

**For builtin Kafka:** after confirming the switch, remove the Kafka pods and their PVCs.

**For external Kafka:** clean up the Milvus topics in the external Kafka instance. Milvus topics follow the format `<cluster_prefix>-dml_<seqNo>_<TimeTick><Version>`.

<div class="alert note">

If you plan to switch back to Kafka later, clean up the data/topics first to avoid conflicts.

</div>

## Switch from Woodpecker to Kafka

<div class="alert warning">

This direction is supported with **Helm** only. With **Milvus Operator**, switching from Woodpecker to Pulsar/Kafka is **not supported** — the Operator does not allow pre-configuring the Kafka connection address that the switch requires.

</div>

### Step 1: Verify the Milvus instance is running

Ensure your Milvus cluster is running properly.

### Step 2: Configure the target Kafka connection

Render the Kafka access configuration into Milvus and enable the target MQ. The `streaming.enabled=true` flag is required for the Switch MQ feature. Create or edit `values.yaml`:

```yaml
extraConfigFiles:
  user.yaml: |+
    kafka:
      brokerList:
        - <your_kafka_address>:<your_kafka_port>
      saslUsername:
      saslPassword:
      saslMechanisms: PLAIN
      securityProtocol: SASL_SSL
```

```shell
helm upgrade -i my-release milvus/milvus \
  --set kafka.enabled=true \
  --set woodpecker.enabled=false \
  --set streaming.enabled=true \
  -f values.yaml
```

Wait for all pods to be ready, then verify that the Kafka access configuration has been rendered into the Milvus configuration. For SASL/SSL details, see [Connect to Kafka with SASL/SSL](connect_kafka_ssl.md).

### Step 3: Execute the MQ switch

<div class="alert note">

Ensure the target Kafka does not contain Milvus topics from a previous configuration. If this is your first switch to Kafka, skip this note; otherwise clean up residual Milvus topics with the same names first.

</div>

```shell
curl -X POST http://<mixcoord_addr>:<mixcoord_port>/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "kafka"}'
```

### Step 4: Verify the switch is complete

```shell
kubectl logs <mixcoord-pod>  | grep "successfully updated mq.type configuration in etcd"
```

A successful switch logs `[mqTypeValue=kafka]`.

### Step 5: (Optional) Clean up Woodpecker data

Delete the Woodpecker data on MinIO/S3 (under `<rootPath>/wp/...`, typically `files/wp/...`) and the Woodpecker metadata in etcd (`etcdctl get woodpecker --prefix`). If you plan to switch back to Woodpecker later, clean up these files first.

## Supported scenarios

| Source MQ | Target MQ | Helm | Milvus Operator |
|-----------|-----------|------|-----------------|
| Builtin Kafka | Woodpecker (MinIO) | **Supported** | **Supported** |
| External Kafka | Woodpecker (MinIO) | **Supported** | **Supported** |
| Woodpecker (MinIO) | External Kafka | **Supported** | **Not supported** |
| Kafka | Woodpecker (local) | **Supported but not recommended** (all pods need a shared FS) | **Not supported** |
