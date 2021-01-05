---
id: overview.md
title: Milvus Overview
sidebar_label: Milvus Overview
---

# Milvus Overview

## What is Milvus

Milvus is an open source similarity search engine for massive-scale vector datasets. Built with heterogeneous computing architecture for the best cost efficiency. Searches over billion-scale vectors take only milliseconds with minimum computing resources.

## Key features

- Heterogeneous computing

  Milvus is designed with heterogeneous computing architecture for the best performance and cost efficiency.

- Multiple indexes

  Milvus supports a variety of indexing types that employs quantization-based, tree-based, and graph-based indexing techniques.

- Intelligent resource management

  Milvus automatically adapts search computation and index building processes based on your datasets and available resources.

- Horizontal scalability

  Milvus supports online / offline expansion to scale both storage and computation resources with simple commands.

- High availability

  Milvus supports WAL (Write-Ahead Logging), which ensures the atomicity and durability of data operations. Milvus is integrated with the Kubernetes framework so that all single point of failures could be avoided for distributed scenarios.

- High compatibility

  Milvus is compatible with almost all deep learning models. Milvus supports multiple programming languages such as Python, Java, C++, and Go. Milvus also supports RESTful API.

- Ease of use

  Milvus can be easily installed in a few steps and enables you to exclusively focus on feature vectors.

- Visualized monitor

  You can track system performance on Prometheus-based GUI monitor dashboards.


## Overall architecture

![Milvus architecture](https://raw.githubusercontent.com/milvus-io/docs/master/assets/milvus_arch.png)
