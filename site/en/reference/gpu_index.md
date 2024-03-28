---
id: gpu_index.md
related_key: gpu_index
summary: GPU index mechanism in Milvus.
---

# GPU Index

Milvus supports various GPU index types to accelerate search performance and efficiency, especially in high-throughput, low-latency, and high-recall scenarios. This topic provides an overview of the GPU index types supported by Milvus, their suitable use cases, and performance characteristics. For information on building indexes on GPU, refer to [Index with GPU](index-with-gpu.md).

GPU acceleration can greatly improve the search performance and efficiency of Milvus, especially for high-throughput, low-latency and high-recall scenarios, and is also very friendly to large nq batch search secnario.

![performance](../../../assets/gpu_index.png)

Milvus' GPU support is contributed by Nvidia [RAPIDS](https://rapids.ai/) team. The following are the GPU index types currently supported by Milvus.

## GPU_CAGRA

- **Description**: A graph-based index optimized for inference GPUs.
- **Suitable for**: Scenarios with a small number of queries where training GPUs with lower memory frequency may not yield optimal results.
- **Performance**: Efficient on inference GPUs.

## GPU_IVF_FLAT & GPU_IVF_PQ

- **Description**: Quantization-based indexes that organize vector data into clusters and employ product quantization for efficient search.
- **Suitable for**: Scenarios requiring fast queries and a balance between accuracy and speed, while managing limited memory resources.
- **Performance**: Provides a balance between speed and accuracy.

## GPU_BRUTE_FORCE

- **Description**: An index that guarantees a recall of 1 by comparing each query with all vectors in the dataset, requiring only the metric type (__metric_type__) and top-k (__limit__) as index building and search parameters.
- **Suitable for**: Scenarios where extremely high recall is crucial.
- **Performance**: Requires memory equal to the size of the original data.

## Conclusion

Currently, Milvus loads all indexes into GPU memory for efficient search operations. The amount of data that can be loaded depends on the size of the GPU memory:

- **GPU_CAGRA**: Memory usage is approximately 1.8 times that of the original vector data.
- **GPU_IVF_FLAT** and **GPU_BRUTE_FORCE**: Requires memory equal to the size of the original data.
- **GPU_IVF_PQ**: Utilizes a smaller memory footprint, which depends on the compression parameter settings.
