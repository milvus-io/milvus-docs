---

id: monitoring_metrics.md
title: Monitoring Metrics
sidebar_label: Monitoring Metrics

---

# Monitoring Metrics

## Metrics Overview

The Milvus dashboard provides details about your application and database configuration. It helps you optimize Milvus performance by monitoring the following areas: 

| Area             | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| Performance Metrics | Important metrics about Milvus performance.                |
| Hardware Metrics | Metrics about CPU/GPU usage, network traffic.              |
| Storage Metrics  | Metrics about data size, storage capacity and total files. |

## Performance Metrics

| Metric                    | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| <b>Insert per Second</b>     | Number of vectors that are inserted in a second. (Real-time display) |
| <b>Queries per Minute</b>    | Number of queries that are run in a minute. (Real-time display) |
| <b>Query Time per Vector</b> | Average time to query one vector. Divide the query elapsed time by the number of queried vectors. |
| <b>Query Service Level</b>   | A system wide metric. Query service level (%) = n_queries_completed_within_threshold1 / n_queries <br/>Generally, it is recommended to set 3 time periods - threshold1, threshold2 and threshold3, to track the query service level. |
| <b>Uptime</b>                | How long Milvus has been running. (Minutes)                  |

## Hardware Metrics

| Metric                | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| <b>GPU Utilization</b>   | GPU utilization ratio (%).                                   |
| <b>GPU Memory Usage</b>  | GPU memory (GB) currently consumed by Milvus.                |
| <b>CPU Utilization</b>   | Divide the time that the server is busy by the total elapsed time. |
| <b>Memory Usage</b>      | Memory (GB) currently consumed by Milvus.                    |
| <b>Cache Utilization</b> | Cache utilization ratio (%).                                 |
| <b>Network IO</b>        | Network IO read/write speed (per second).                    |
| <b>Disk Read Speed</b>   | Disk read speed (GB/s).                                      |
| <b>Disk Write Speed</b>  | Disk write speed (GB/s).                                     |

## Storage Metrics

| Metric         | Description                                      |
| -------------- | ------------------------------------------------ |
| <b>Data Size</b>  | Total amount of data stored in Milvus.           |
| <b>Total File</b> | Number of data files currently stored in Milvus. |

## Related links
[Monitoring and Alerting](../guides/monitor.md)

