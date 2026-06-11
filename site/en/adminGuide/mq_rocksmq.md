---
id: mq_rocksmq.md
title: RocksMQ
---

# Use RocksMQ as the Milvus Message Queue

RocksMQ is an embedded message queue (WAL) bundled with Milvus, available for **Milvus Standalone only**. It was the default message queue for standalone deployments up to 2.5.x; from 2.6.x, Milvus Standalone uses embedded [Woodpecker](woodpecker.md) by default.

## Version compatibility

- **Standalone only** — RocksMQ is **not** supported in Milvus Distributed (cluster). See the [message queue support matrix](mqtype-overview.md#Supported-message-queues).
- RocksMQ ships with Milvus, so there is no separate version to install.
- It was the default standalone message queue up to 2.5.x, and is superseded by embedded Woodpecker from 2.6.x onward.

## Deploy Milvus Standalone with RocksMQ using Docker

### Install

Follow [Run Milvus in Docker](install_standalone-docker.md). On Milvus 2.6.x and later the standalone default is Woodpecker, so set the message-queue type to RocksMQ explicitly:

```bash
mkdir milvus-rocksmq && cd milvus-rocksmq
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh

# Create user.yaml to use RocksMQ
cat > user.yaml <<'EOF'
mq:
  type: rocksmq
EOF

bash standalone_embed.sh start
```

### Configure

To tune RocksMQ, add a `rocksmq` section to `user.yaml` and restart the service:

```yaml
mq:
  type: rocksmq
rocksmq:
  path: /var/lib/milvus/rdb_data   # where messages are stored
  lrucacheratio: 0.06              # rocksdb cache memory ratio
  rocksmqPageSize: 67108864        # 64 MB, size of each message page
  retentionTimeInMinutes: 4320     # 3 days
  retentionSizeInMB: 8192          # 8 GB
  compactionInterval: 86400        # 1 day, trigger rocksdb compaction
  compressionTypes: [0, 0, 7, 7, 7]
```

```bash
bash standalone_embed.sh restart
```

### Uninstall

```bash
bash standalone_embed.sh stop
bash standalone_embed.sh delete
```

## Notes

- **Upgrading from 2.5.x to 2.6.x:** {{fragments/mq_upgrade_limitation.md}} Because 2.6.x changes the standalone default to Woodpecker, pin `mq.type: rocksmq` in your `user.yaml` **before** upgrading if you want to keep RocksMQ.
- To change the message queue of a running instance, see [Switch from RocksMQ to Woodpecker](switch-rocksmq-woodpecker.md).

## What's next

- [Woodpecker (default message queue)](woodpecker.md)
- [Switch from RocksMQ to Woodpecker](switch-rocksmq-woodpecker.md)
