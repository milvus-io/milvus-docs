---
id: msgstream.md
title: Specify Message Stream System
summary: Learn how to configure and specify the message stream system in Milvus.
---

# Specify Message Stream System

Milvus supports three types of message stream systems: RocksMQ(based on RocksDB implementation), Puslar and Kafka. You can choose a particular message stream system for your unique business requirements. The default message stream system in Milvus standalone is RocksMQ while the default message stream system in Milvus cluster is Pulsar.

This topic describes how to configure and specify the message stream system in Milvus.

## Limitations

The table below shows whether the three types of message stream systems are supported in Milvus standalone and cluster deployment mode.

|                 | RocksMQ | Pulsar | Kafka |
|:---------------:|:-------:|:------:|:-----:|
| Standalone mode |    ✔️    |    ✔️   |   ✔️   |
|   Cluster mode  |    ✖️    |    ✔️   |   ✔️   |


There are also other limitations for specifying the message stream system:
- Only one message stream system for one Milvus instance is supported. However we still have backward compatibility with multiple systems set for one instance. The priority is as follows:
  -  standalone mode:  RocksMQ(default) > Pulsar > Kafka
  - cluster mode: Pulsar(default) > Kafka
- The message stream system cannot be changed while the system is running. 
-  Only Kafka 2.x or 3.x verison is supported.

## Specify message stream system

### Specify in YAML file

Although Milvus supports multiple types of message stream systems, it is recommended that you configure one type of message stream system within the `milvus.yaml` file at a time. 

Pulsar is enabled by default under cluster mode, and RocksMQ is enabled by default under standalone mode. 

```YAML
pulsar:
  address: localhost # Address of pulsar
  port: 6650 # Port of pulsar
  maxMessageSize: 5242880 # 5 * 1024 * 1024 Bytes, Maximum size of each message in pulsar.

#kafka:
#  brokerList: localhost1:9092,localhost2:9092,localhost3:9092

rocksmq:
  path: /var/lib/milvus/rdb_data # The path where the message is stored in rocksmq
  rocksmqPageSize: 2147483648 # 2 GB, 2 * 1024 * 1024 * 1024 bytes, The size of each page of messages in rocksmq
  retentionTimeInMinutes: 10080 # 7 days, 7 * 24 * 60 minutes, The retention time of the message in rocksmq.
  retentionSizeInMB: 8192 # 8 GB, 8 * 1024 MB, The retention size of the message in rocksmq.
```

Add the code below in the `milvus.yaml` file to enable Kafka.

```YAML
kafka:
  brokerList: localhost:9092
```

When RocksMQ is enabled under standalone mode, the system will fail is you switch to the cluster mode using RocksMQ.

```YAML
rocksmq:
  path: /var/lib/milvus/rdb_data # The path where the message is stored in rocksmq
  rocksmqPageSize: 2147483648 # 2 GB, 2 * 1024 * 1024 * 1024 bytes, The size of each page of messages in rocksmq
  retentionTimeInMinutes: 10080 # 7 days, 7 * 24 * 60 minutes, The retention time of the message in rocksmq.
  retentionSizeInMB: 8192 # 8 GB, 8 * 1024 MB, The retention size of the message in rocksmq.
```

### Specify with Milvus Helm

1. Set the message stream system for Milvus standalone.

Run to following code to set RocksMQ as the message stream system.

```
helm install release milvus/milvus --set cluster.enabled=false --set pulsar.enabled=false --set minio.mode=standalone --set etcd.replicaCount=1
```

Run to following code to set Pulsar as the message stream system.

```
helm install release milvus/milvus --set cluster.enabled=false --set pulsar.enabled=true --set minio.mode=standalone --set etcd.replicaCount=1 --set standalone.messageQueue=pulsar
```

Run to following code to set Kafka as the message stream system.

```
helm install release milvus/milvus --set cluster.enabled=false --set pulsar.enabled=false --set minio.mode=standalone --set etcd.replicaCount=1 --set kafka.enabled=true --set standalone.messageQueue=kafka
```

2. Set the message stream system for Milvus standalone.

Run to following code to set Pulsar as the message stream system.

```
helm install release milvus/milvus
```

Run to following code to set Kafka as the message stream system.

```
helm install release milvus/milvus --set pulsar.enabled=false --set kafka.enabled=true
```

### Specify with Milvus Operator

1. Set the message stream system for Milvus standalone.

Currently, only RocksMQ is supported when configuring with Milvus Operator. Run the following code to set RocksMQ as the message stream system under standalone mode.

```
# manifest.yaml: kubectl create -f manifest.yaml
apiVersion: milvus.io/v1alpha1
kind: Milvus
metadata:
  name: milvus
spec:
  dependencies: {}
  config: {}
```

2. Set the message stream system for Milvus cluster.

Run to following code to set Pulsar as the message stream system.

```
# manifest.yaml: kubectl create -f manifest.yaml
apiVersion: milvus.io/v1alpha1
kind: MilvusCluster
metadata:
  name: milvus
spec:
  dependencies: {}
  components: 
    msgStreamType: pulsar
    pulsar: {}
  config: {}
```

Run to following code to set Kafka as the message stream system.

```
# manifest.yaml: kubectl create -f manifest.yaml
apiVersion: milvus.io/v1alpha1
kind: MilvusCluster
metadata:
  name: milvus
spec:
  dependencies: {}
  components: 
    msgStreamType: kafka
    kafka: {}
  config: {}
```

## What's next
- Learn about the [Milvus architecture](architecture_overview.md).
- Learn how to [configure Milvus](configure-docker.md)
- Learn to [configure Milvus dependencies with Milvus Operator](operator.md).



