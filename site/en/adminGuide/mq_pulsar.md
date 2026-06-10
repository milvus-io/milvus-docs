---
id: mq_pulsar.md
title: Pulsar
---

# Use Pulsar as the Milvus Message Queue

Apache Pulsar is one of the message-queue (WAL) backends Milvus supports. Starting from Milvus 2.6.x, **Woodpecker** is the default and recommended message queue; Pulsar remains fully supported for users who prefer it.

## Supported versions

- Milvus Distributed supports Pulsar as the message queue.
- Since Milvus 2.5, the Milvus Helm chart and Milvus Operator deploy Pulsar v3 by default, while Pulsar v2 remains compatible. See [Upgrade to Pulsar v3](upgrade-pulsar-v3.md) and [Continue Using Pulsar v2](use-pulsar-v2.md).

## Install Milvus with Pulsar (Helm)

To deploy a Milvus cluster with Pulsar instead of Woodpecker, install the Helm chart without disabling Pulsar:

```bash
helm install my-release zilliztech/milvus \
  --set image.all.tag=v{{var.milvus_release_version}} \
  --set streaming.enabled=true \
  --set indexNode.enabled=false
```

### Kubernetes v1.25+ PodDisruptionBudget workaround

On Kubernetes v1.25 and later, the bundled Pulsar sub-chart may run into PodDisruptionBudget API issues. If you encounter them, disable the Pulsar PodDisruptionBudget policies:

```bash
helm install my-release zilliztech/milvus \
  --set pulsar.bookkeeper.pdb.usePolicy=false \
  --set pulsar.broker.pdb.usePolicy=false \
  --set pulsar.proxy.pdb.usePolicy=false \
  --set pulsar.zookeeper.pdb.usePolicy=false
```

## Configure Pulsar

For detailed Pulsar parameters across deployment methods, see:

- [Configure Pulsar with Docker Compose or Helm](deploy_pulsar.md)
- [Configure Pulsar with Milvus Operator](message_storage_operator.md#Configure-Pulsar)

## What's next

- [Woodpecker (default message queue)](woodpecker.md)
- [Switch MQ Type for Milvus Cluster](switch_milvus_cluster_mq_type-helm.md)
