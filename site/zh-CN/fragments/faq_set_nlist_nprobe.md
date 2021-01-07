IVF 索引的 <code>nlist</code> 值需要根据具体的使用情况去设置。一般来说，推荐值为 <code>4 &times; sqrt(n)</code>，其中 n 为 segment 内的 entity 总量。

`nprobe` 的选取需要根据数据总量和实际场景在速度性能和准确率之间进行取舍。建议通过多次实验确定一个合理的值。

以下是使用公开测试数据集 sift50m 针对 `nlist` 和 `nprobe` 的一个测试。以索引类型 IVF\_SQ8 为例，针对不同 `nlist`/`nprobe` 组合的搜索时间和召回率分别进行对比。

<div class="alert note">

因 CPU 版 Milvus 和 GPU 版 Milvus 测试结果类似，此处仅展示基于 GPU 版 Milvus 测试的结果。

</div>

<img src="https://github.com/milvus-io/docs/blob/master/v0.11.0/assets/accuracy_nlist_nprobe.png" alt="accuracy_nlist_nprobe.png">

在本次测试中，`nlist` 和 `nprobe` 的值成比例增长，召回率随 `nlist`/`nprobe` 组合增长呈现上升的趋势。

<img src="https://github.com/milvus-io/docs/blob/master/v0.11.0/assets/performance_nlist_nprobe.png" alt="performance_nlist_nprobe.png">

在 `nlist` 为 4096 和 `nprobe` 为 128 时，速度性能最佳。
