---
id: mqtype-overview.md
title: Message Queue Overview
summary: Overview of the message queue (mqType) options Milvus supports, and which one to use for standalone vs. distributed deployments.
---

# Message Queue Overview

Milvus relies on a message queue (write-ahead log, WAL) to manage logs of recent changes, output stream logs, and provide log subscriptions. Starting from Milvus 2.6.x, **Woodpecker** is the default message queue and requires no separate messaging infrastructure. Pulsar, Kafka, and RocksMQ remain supported for specific scenarios.

## Supported message queues

| Message queue | Milvus Standalone | Milvus Distributed (cluster) | Default in | Notes |
| --- | :---: | :---: | --- | --- |
| [Woodpecker](woodpecker.md) | ✔️ (embedded) | ✔️ (embedded or service) | **2.6.x and later** (both modes) | Default and recommended. Cloud-native WAL on object storage; no external service required. |
| [Pulsar](mq_pulsar.md) | ✔️ | ✔️ | ≤ 2.5.x (cluster default) | Supported, external or bundled. |
| [Kafka](mq_kafka.md) | ✔️ | ✔️ | — | Supported. Only Kafka 2.x or 3.x. |
| [RocksMQ](mq_rocksmq.md) | ✔️ | ✖️ | ≤ 2.5.x (standalone default) | Supported for **standalone only**. |

<div class="alert note">

- Each Milvus instance uses exactly one message queue.
- {{fragments/mq_upgrade_limitation.md}}
- To change the message queue of a running instance, see [Switch MQ Type](switch_milvus_cluster_mq_type-helm.md) (supported from v2.6.14).

</div>

## Choosing a message queue

- **New deployments (2.6.x / 3.x):** use **Woodpecker** (the default). Standalone runs it embedded; distributed can run it embedded or as a dedicated [service](woodpecker.md#Deployment-modes).
- **Existing Pulsar or Kafka users:** Pulsar and Kafka remain fully supported. Keep them, or [switch to Woodpecker](switch_milvus_cluster_mq_type-helm.md).
- **RocksMQ:** standalone only, and superseded by embedded Woodpecker from 2.6.x onward.
