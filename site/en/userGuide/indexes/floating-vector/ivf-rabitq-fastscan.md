---
id: ivf-rabitq-fastscan.md
title: "IVF_RABITQ_FASTSCAN"
summary: "IVF_RABITQ_FASTSCAN combines IVF, RaBitQ binary quantization, and SIMD batch scanning to provide memory-efficient, high-throughput vector search."
beta: Milvus 3.0.x
---

# IVF_RABITQ_FASTSCAN

`IVF_RABITQ_FASTSCAN` combines IVF partitioning, RaBitQ binary quantization, and FastScan batch processing. It stores one-bit RaBitQ codes for database vectors and processes the codes in SIMD-friendly blocks of 32 database vectors. This makes it a good choice for high-throughput, memory-constrained workloads that can accept approximate results.

Choose `IVF_RABITQ_FASTSCAN` over [IVF_RABITQ](ivf-rabitq.md) when searches scan many candidates and throughput is the primary goal. FastScan's per-query setup cost is amortized across packed code blocks, so it is typically more beneficial for large datasets or long IVF lists. For small collections or searches that inspect few candidates, use `IVF_RABITQ` instead. It also supports configurable query quantization, more refinement types, and iterators.

## How it works

`IVF_RABITQ_FASTSCAN` uses the following stages:

1. **IVF partitioning**: IVF groups vectors into `nlist` clusters and searches the `nprobe` closest clusters.
1. **RaBitQ encoding**: Each vector residual is encoded as a one-bit-per-dimension RaBitQ code.
1. **FastScan**: The index packs codes for cache-friendly, SIMD batch processing. It evaluates 32 database vectors in each batch.
1. **Optional refinement**: When enabled, an FP32 refiner re-scores candidates before Milvus returns the final results.

The underlying Faiss index is `IndexIVFRaBitQFastScan`. Knowhere wraps it with a random rotation transform and optionally adds an FP32 refiner.

FastScan performs per-query setup work, such as building and quantizing query-related lookup tables, before scanning packed code blocks. Benchmark both `IVF_RABITQ` and `IVF_RABITQ_FASTSCAN` with your data and search parameters.

## Build index

Use `IVF_RABITQ_FASTSCAN` as the index type. The index supports `COSINE`, `L2`, and `IP` metrics.

```python
from pymilvus import MilvusClient

index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name="your_vector_field_name",
    index_type="IVF_RABITQ_FASTSCAN",
    index_name="vector_index",
    metric_type="L2",
    params={
        "nlist": 1024,
        "refine": True,
        "refine_type": "FP32",
    },
)
```

`refine_type` is optional. If refinement is enabled, it must be `FP32` (or `flat`); other refinement types are not supported.

## Search on index

Set `nprobe` to control how many IVF clusters are searched. If the index was built with refinement, use `refine_k` to control the candidate pool passed to the FP32 refiner.

```python
search_params = {
    "params": {
        "nprobe": 128,
        "refine_k": 2,
    }
}

res = MilvusClient.search(
    collection_name="your_collection_name",
    anns_field="vector_field",
    data=[[0.1, 0.2, 0.3, 0.4, 0.5]],
    limit=3,
    search_params=search_params,
)
```

## Index params

### Index building params

| Parameter | Description | Value range | Default |
| --- | --- | --- | --- |
| `nlist` | Number of IVF clusters. Larger values create smaller partitions and increase build time. | Integer `[1, 65536]` | `128` |
| `refine` | Enables FP32 refinement. | `true`, `false` | `false` |
| `refine_type` | Representation used by the refiner. Required only when `refine` is `true`. | `FP32`, `flat` | None |

### Index-specific search params

| Parameter | Description | Value range | Default |
| --- | --- | --- | --- |
| `nprobe` | Number of IVF clusters to search. Higher values usually improve recall and increase latency. | Integer `[1, nlist]` | `8` |
| `refine_k` | Multiplier for the number of candidates sent to the FP32 refiner. Has no effect if refinement is disabled. | Float `[1, float_max)` | `1` |

## Limitations

- FastScan uses a fixed 1-bit RaBitQ database encoding and 8-bit query quantization. `rbq_bits_query` must be omitted or set to `0`.
- Only FP32/flat refinement is supported.
- Iterators are not supported.
- This is a CPU index. It does not run on GPU.
- Actual performance depends on CPU SIMD support, vector dimension, `nlist`, `nprobe`, and data distribution. Benchmark it with your workload before deploying it to production.

For the non-FastScan RaBitQ variant and its additional refinement options, see [IVF_RABITQ](ivf-rabitq.md).
