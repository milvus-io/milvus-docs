一般而言，Milvus 对单个数据段内的查询是并行的，多个数据段的处理根据发行版本略有不同。

假设一个集合存在多个数据段，当查询请求到达时：

- CPU 版 Milvus 会对数据段读取任务和段内查询任务进行流水线处理。
- GPU 版 Milvus 会在 CPU 版的基础上，将多个数据段分配给各个 GPU 处理。

可参阅文章：<a href="https://zhuanlan.zhihu.com/p/110332250">Milvus 开源向量搜索引擎 ANNS</a>。