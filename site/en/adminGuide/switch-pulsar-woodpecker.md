---
id: switch-pulsar-woodpecker.md
title: Switch between Pulsar and Woodpecker
summary: Switch the message queue of a Milvus cluster between Pulsar and Woodpecker, with Helm or Milvus Operator.
---

# Switch between Pulsar and Woodpecker

This page describes how to switch the message queue (MQ) of a **Milvus cluster** between **Pulsar** (builtin or external) and **Woodpecker** (MinIO backend), in both directions, for Helm and Milvus Operator deployments. For the general workflow and prerequisites, see [Switch MQ Type](switch-mq-type.md).

## Switch from Pulsar to Woodpecker

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

### Step 5: (Optional) Stop Pulsar and clean up

**For builtin Pulsar (Helm):** disable Pulsar and enable Woodpecker, then delete the Pulsar PVCs.

```shell
helm upgrade my-release zilliztech/milvus \
  --set image.all.tag=v{{var.milvus_release_version}} \
  --set pulsarv3.enabled=false \
  --set woodpecker.enabled=true \
  --set streaming.enabled=true \
  --set indexNode.enabled=false
```

```shell
kubectl get pvc | grep my-release-pulsarv3
kubectl delete pvc <pulsar-pvc-name> ...
```

**For builtin Pulsar (Operator):** `helm uninstall my-release-pulsar`, then delete the Pulsar PVCs.

**For external Pulsar:** clean up the Milvus topics in the external Pulsar instance. Milvus topics follow the format `<cluster_prefix>-dml_<seqNo>_<TimeTick><Version>` (for example, `by-dev-rootcoord-dml_10_464633776992639586v0`).

<div class="alert note">

If you plan to switch back to Pulsar later, clean up the data/topics first to avoid conflicts. Due to Helm chart limitations, switching back to a **builtin** Pulsar instance is currently not possible.

</div>

## Switch from Woodpecker to Pulsar

<div class="alert warning">

This direction is supported with **Helm** only. With **Milvus Operator**, switching from Woodpecker to Pulsar/Kafka is **not supported** — the Operator does not allow pre-configuring the Pulsar connection address that the switch requires.

</div>

### Step 1: Verify the Milvus instance is running

Ensure your Milvus cluster is running properly.

### Step 2: Configure the target Pulsar connection

Render the Pulsar access configuration into Milvus and enable the target MQ. The `streaming.enabled=true` flag is required for the Switch MQ feature. Create or edit `values.yaml`:

```yaml
extraConfigFiles:
  user.yaml: |+
    pulsar:
      address: <pulsar addr>
      port: <pulsar port, e.g. 6650>
```

```shell
helm upgrade -i my-release zilliztech/milvus \
  --set pulsarv3.enabled=true \
  --set woodpecker.enabled=false \
  --set streaming.enabled=true \
  -f values.yaml
```

Wait for all pods to be ready, then verify that the Pulsar access configuration has been rendered into the Milvus configuration.

### Step 3: Execute the MQ switch

<div class="alert note">

Ensure the target Pulsar does not contain Milvus topics from a previous configuration. If this is your first switch to Pulsar, skip this note; otherwise clean up residual Milvus topics with the same names first.

</div>

```shell
curl -X POST http://<mixcoord_addr>:<mixcoord_port>/management/wal/alter \
  -H "Content-Type: application/json" \
  -d '{"target_wal_name": "pulsar"}'
```

### Step 4: Verify the switch is complete

```shell
kubectl logs <mixcoord-pod>  | grep "successfully updated mq.type configuration in etcd"
```

A successful switch logs `[mqTypeValue=pulsar]`.

### Step 5: (Optional) Clean up Woodpecker data

Delete the Woodpecker data on MinIO/S3 (under `<rootPath>/wp/...`, typically `files/wp/...`) and the Woodpecker metadata in etcd (`etcdctl get woodpecker --prefix`). If you plan to switch back to Woodpecker later, clean up these files first.

## Supported scenarios

| Source MQ | Target MQ | Helm | Milvus Operator |
|-----------|-----------|------|-----------------|
| Builtin Pulsar | Woodpecker (MinIO) | **Supported** | **Supported** |
| External Pulsar | Woodpecker (MinIO) | **Supported** | **Supported** |
| Woodpecker (MinIO) | External Pulsar | **Supported** | **Not supported** |
| Pulsar | Woodpecker (local) | **Supported but not recommended** (all pods need a shared FS) | **Not supported** |
