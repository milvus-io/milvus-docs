---
id: overview.md
title: Milvus Overview
sidebar_label: Milvus Overview
---

# Milvus 简介

## Milvus 是什么

Milvus 是一款开源向量相似度搜索引擎，建立在 Faiss、NMSLIB、Annoy 等向量索引库基础之上，具有功能强大、稳定可靠以及易于使用等特点。Milvus 集成了这些向量索引库，隐藏了他们的复杂性，提供了一套简单而一致的 API。此外，Milvus 能够有效的管理向量数据，提供针对向量和非向量数据的增删改查的能力。除了提供针对向量的近实时搜索能力外，Milvus 可以对标量数据进行过滤。随着数据和查询规模的增加，Milvus 还提供了集群分片的解决方案，支持读写分离、水平扩展、动态扩容等功能，实现了对于超大数据规模的支持。目前，Milvus 是一个单节点主从式架构（Client-server model）的服务器，最高可以支持 TB 级特征数据的存储和搜索服务。对于有更大数据规模或者高并发需求的用户，可以使用目前尚在实验阶段的集群分片中间件 Mishards 进行部署。

在服务端，Milvus 由两部分组成：Milvus server 和 Meta store。

* Milvus server 提供了 Milvus 的主要功能，包括数据的存储与管理、数据的搜索等。
* Meta store 则存储了 Milvus 的元数据。目前 Milvus 支持的元数据库可以是 MySQL 和 SQLite。

这些能力使得 Milvus 可以广泛地应用于以下场景：

- 图像、视频、音频等音视频搜索领域
- 文本搜索、推荐和交互式问答系统等文本搜索领域
- 新药搜索、基因筛选等生物医药领域

除了提供核心的数据管理和搜索功能外，Milvus 还提供了

- 基于 JSON 的 DSL，提供用户灵活方便的搜索方式
- 基于 Python / Java / Go / C++ 的 SDK 和 RESTful API
- 对接基于 Prometheus 的监控与告警系统
- 基于 Docker和 Kubernetes 的部署方式

以上功能都极大地增强了 Milvus 的易用性。

Milvus 是开箱即用的产品，所有配置参数都有默认值。因此对初学者来说使用体验非常友好。随着深入了解 Milvus，你会发现整个 Milvus 都是灵活可配置的。你可以利用 Milvus 的高级特性来优化向量的存储与搜索，更好地服务于你的业务。

Milvus 在 Apache 2 License 协议下发布，于 2019 年 10 月正式开源，是 [LF AI](https://lfai.foundation/) 基金会的孵化项目。Milvus 的源代码被托管于 Github 之上：[Milvus · 开源的特征向量相似度搜索引擎](https://github.com/milvus-io/milvus)。如果你想加入我们的开发者社区，欢迎访问：[Contribute to Milvus](https://github.com/milvus-io/milvus/blob/master/CONTRIBUTING.md#contributing-to-milvus)。

如果你对 Milvus 有任何与功能、SDK 等相关的问题，欢迎加入 [Slack](https://join.slack.com/t/milvusio/shared_invite/zt-e0u4qu3k-bI2GDNys3ZqX1YCJ9OM~GQ) 参与讨论。

## 主要特性

- 全面的相似度指标
  
  Milvus 支持各种常用的相似度计算指标，包括欧氏距离、内积、汉明距离和杰卡德距离等。你可以根据应用需求来选择最有效的向量相似度计算方式。

- 业界领先的性能

  Milvus 基于高度优化的 Approximate Nearest Neighbor Search (ANNS) 索引库构建，包括 faiss、 annoy、和 hnswlib 等。你可以针对不同使用场景选择不同的索引类型。

- 动态数据管理
  
  你可以随时对数据进行插入、删除、搜索、更新等操作而无需受到静态数据带来的困扰。

- 近实时搜索

  近实时搜索指的是，插入 Milvus 的数据在默认 1 秒后即被存入存储设备并能被搜索到。详情请参阅 [Search](../search/index.md)。

- 高成本效益
  
  Milvus 充分利用现代处理器的并行计算能力，可以在单台通用服务器上完成对十亿级数据的毫秒级搜索。

- 支持多种数据类型和高级搜索（即将上线）
  
  Milvus 的数据记录中的字段支持多种数据类型。你还可以对一个或多个字段使用高级搜索，例如过滤、排序和聚合。

- 高扩展性和可靠性
  
  你可以在分布式环境中部署 Milvus。如果要对集群扩容或者增加可靠性，你只需增加节点。

- 云原生

  你可以轻松在公有云、私有云、或混合云上运行 Milvus。

- 简单易用

  Milvus 提供了易用的 Python、Java、Go 和 C++ SDK，另外还提供了 RESTful API。

- 预写式日志

  Milvus 实现了类似数据库系统的 WAL（预写式日志，Write Ahead Log）。任何对于数据的修改操作在进入 Milvus 之前会先存储成为日志，然后再写入 Milvus。一旦在写入 Milvus 过程中遭遇失败（如磁盘空间不足、内存耗尽），Milvus 重启时会从日志中恢复之前没有完成的操作，重新执行。详情请参阅 [预写式日志](../write-ahead-log/write-ahead-log.md)。

- DSL

  Milvus 提供了基于 JSON 结构的 DSL（领域特定语言，Domain-specific language）。你可以使用 DSL 灵活地进行查询。详情请参阅 [API & DSL](../api/index.md)。

- Mishards

  Mishards 是一个用 Python 开发的 Milvus 集群分片中间件，可处理请求转发、读写分离、水平扩展、动态扩容（使得内存和算力可以无限扩容）。详情请参阅 [Mishards](../mishards/index.md)。

- 异构计算

  Milvus 能够调度多个 GPU 进行向量搜索和索引建立。利用 GPU 强大的并行运算能力，Milvus 在大批量查询和向量索引建立等高耗时任务上性能表现优异。详情请参阅 [异构计算](../heterogeneous-computing/index.md)。

- 向量索引

  Milvus 支持基于 Faiss、NMSLIB 和 Annoy 的树、图和量化等多种索引。关于向量索引的详情，请参阅 [向量索引](../vector-index/overview.md)。
而对于索引的选择和索引参数的选择，请参阅 [性能调优](../advanced-tuning/index.md)。

- 监控与告警

  Milvus 使用 Prometheus 作为监控和性能指标存储方案，使用 Grafana 作为可视化组件进行数据展示。详情请参阅 [监控](../metrics/prometheus-collection-metrics.md)。

## 术语

- 实体（Entity）: 代表一个实际对象，由字段组成。

- 字段（Field）：用于表示对象的某个属性。字段可以是结构化数据，也可以是向量。

- 实体标识（Entity ID）: 是用于唯一指代一个实体的 64 位非负整数。创建实体时，该标识可以由用户指定，也可以由 Milvus 自动生成。

<div class="alert note">
目前，Milvus 不支持标识去重，因此你需要保证插入实体标识的唯一性。
</div>

- 集合（Collection）: 包含一组同类实体，可以理解为关系型数据库系统中的表。

- 段（Segment）: 为了能处理大规模的数据，Milvus 会将数据分段。一个集合可以包含多个段。

- 分区（Partition）: 用于将集合中的数据划分为几个独立的部分。

- 索引（Index）：一种加速数据检索的数据结构。

- 映射（Mapping）: 一个集合中数据的组织形式，可以理解为关系型数据库系统中的 Schema。

- 向量（Vector）：一种由 N 维数组成的数据类型。是事物特征的抽象，可用于表征某个事物。

<div class="alert note">
注意：目前，一个实体最多只能包含一个向量。
</div>

## 路线图

- 支持字符串类型
    - 支持字符串类型数据的存储
    - 支持字符串比较（`==` 和 `!=`）
    - 支持英文文本的分词和匹配

- 支持实体标识去重

- 自动故障切换和数据冗余

    - 选主和心跳
    - 日志复制
    - 快照复制
    - 索引复制
    - 多组段副本
    - 快速备份和恢复

- 水平扩展

目前，Milvus 已经提供了水平扩展的解决方案 Mishards，但是该方案目前仅仅是实验性质。

- Milvus 备份和恢复工具

    - 数据备份工具
    - 数据恢复工具
    - 数据迁移工具

- 实时搜索

当前，Milvus 提供的是近实时搜索能力。未来 Milvus 会提供实时的数据搜索能力，即只要数据被成功修改，接下来的查询立刻就可见。

- 改进缓存策略

## 整体架构

![Milvus 架构](../../../assets/milvus_arch.png)

## 接下来你可以

- 了解 [特征向量](vector.md), [向量数据库](vector_db.md) 的发展现状和 [向量检索算法](index_method.md)
- 几分钟轻易搞定 [Milvus 安装](../guides/get_started/install_milvus/install_milvus.md)
