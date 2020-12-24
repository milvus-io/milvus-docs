---
id: performance_faq.md
---

# 性能优化问题

## 为什么重启 Milvus 服务端之后，第一次搜索时间非常长？{#1}

重启后第一次搜索时，会将数据从磁盘加载到内存，所以这个时间会比较长。可以在 **milvus.yaml** 中开启 `preload_collection`，在内存允许的情况下尽可能多地加载集合。这样在每次重启服务端之后，数据都会先载入到内存中，可以解决第一次搜索耗时很长的问题。或者在查询前，调用方法 `load_collection()` 将该集合加载到内存。


## 为什么搜索的速度非常慢？{#2}

请首先检查 **milvus.yaml** 的 `cache.cache_size` 参数是否大于集合中的数据量。


## 如何进行性能调优？{#3}

- 确保配置文件中的参数 `cache.cache_size` 值大于集合中的数据量。
- 确保所有数据文件都建立了索引。
- 检查服务器上是否有其他进程在占用 CPU 资源。
- 调整参数 `segment_row_limit` 和 `nlist` 的值。
- 如果检索性能不稳定，可在启动 Milvus 时添加参数 `-e OMP_NUM_THREADS=NUM`，其中 `NUM` 为 CPU 逻辑核数的 2/3。

详见 [性能调优](tuning.md)。


## 建立索引时需要设置 <code>nlist</code> 或 <code>nprobe</code> 值，如何选择该值大小？{#4}

{{fragments/faq_recommendedvalue_nlist_nprobe.md}}

## 为什么有时候小的数据集查询时间反而更长？{#5}

如果数据文件的大小小于创建集合时 `segment_row_limit` 参数的值，Milvus 则不会为此数据文件构建索引。因此，小的数据集有可能查询时间会更长。你还可以调用 `create_index` 建立索引。


## 为什么查询时 GPU 一直空闲？{#6}

{{fragments/faq_gpu_idle.md}}


## 为什么数据插入后不能马上被搜索到？{#7}

因为数据还没有落盘。要确保数据插入后立刻能搜索到，可以手动调用 `flush` 接口。但是频繁调用 `flush` 接口可能会产生大量小数据文件，从而导致查询变慢。


## 为什么我的 CPU 利用率始终不高？{#8}

`nq` = 100 以下，且数据量也不大的时候确实会出现这个现象。Milvus 在计算时，批量内的查询是并行处理的，如果批量不大且数据量也不大的话，并行度不高，CPU 利用率也就不高了。


## Milvus 的导入性能如何？{#9}

客户端和服务端在同一台物理机上时，10 万条 128 维的向量导入需要约 0.8 秒（基于 SSD 磁盘）。这个具体也要看磁盘的 I/O 速度。


## 边插入边搜索会影响搜索速度吗？{#10}

- 当插入向量没有达到建索引条件时，新插入向量在初次被搜索时需要从磁盘加载到内存。
- 当插入向量达到建索引条件时，Milvus 开始为新增向量创建索引。v0.9.0 之后，新出现的搜索请求会打断建索引任务，这需要 1 秒左右的延时。


## 为什么同样的数据量，用 GPU 查询比 CPU 查询慢？{#11}

一般来说，当 `nq`（每次查询的向量条数）较小时，用 CPU 查询比较快。只有当 `nq` 较大（约大于 500）时，用 GPU 查询才会更有优势。

因为在 Milvus 中，每次用 GPU 查询都需要将数据从内存加载到显存。只有当 GPU 查询节省的计算时间能抵消掉数据加载的时间，才能体现出 GPU 查询的优势。

## 仍有问题没有得到解答？{#12}

如果仍有其他问题，你可以：

- 在 GitHub 上访问 [Milvus](https://github.com/milvus-io/milvus/issues)，提问、分享、交流，帮助其他用户。
- 加入我们的 [Slack 社区](https://join.slack.com/t/milvusio/shared_invite/enQtNzY1OTQ0NDI3NjMzLWNmYmM1NmNjOTQ5MGI5NDhhYmRhMGU5M2NhNzhhMDMzY2MzNDdlYjM5ODQ5MmE3ODFlYzU3YjJkNmVlNDQ2ZTk)，与其他用户讨论交流。

