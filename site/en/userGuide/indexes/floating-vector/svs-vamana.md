---
id: svs-vamana.md
title: "SVS_VAMANA"
summary: "SVS_VAMANA is an in-memory, graph-based index built on Intel's Scalable Vector Search (SVS) implementation of the Vamana graph algorithm. It optionally applies LeanVec vector compression, which reduces memory footprint and accelerates distance computation while still reaching very high recall."
---

# SVS_VAMANA

**SVS_VAMANA** is an **in-memory**, **graph-based** index built on Intel's [Scalable Vector Search (SVS)](https://github.com/intel/ScalableVectorSearch) implementation of the **Vamana** graph algorithm — the same graph structure used by [DISKANN](diskann.md), but kept fully in memory and optimized. SVS_VAMANA optionally applies **LeanVec** vector compression, a dimensionality-reduction and quantization technique that reduces memory usage and speeds up search while still reaching very high recall.

## Overview

### Vamana graph

Like DISKANN, SVS_VAMANA builds a single-layer proximity graph in which each vector is a node and edges connect vectors likely to be close neighbors. The graph is built in two passes over the dataset:

1. **Greedy search with backtracking**: For each node **x**, the algorithm searches the graph built so far using a search buffer with capacity `svs_construction_window_size`, recording every visited node.

1. **Neighbor pruning**: The nodes returned by the greedy search become candidate neighbors for **x**. Candidates are considered in order of increasing distance from **x**, and a candidate is kept only if it is not already well covered by a previously-kept, closer candidate — a candidate `c` is skipped once some kept neighbor `n` satisfies `alpha * distance(n, c) <= distance(x, c)`. This favors long-range edges over redundant short-range ones, which is what lets search "jump" across the graph rather than crawl through nearest neighbors. Pruning stops once `svs_graph_max_degree` neighbors have been kept.

1. **Backward edges**: For each neighbor added to **x**, a reverse edge back to **x** is added, so the graph stays well connected in both directions. Neighbors also prune their edges to maintain `svs_graph_max_degree`.

Pruning runs twice: once with `alpha = 1` to establish good initial connections, and once with the configured `svs_alpha` to more aggressively favor long-range edges. A larger `svs_graph_max_degree` and `svs_construction_window_size` produce a denser, higher-quality graph at the cost of more memory and longer build time.

At search time, the algorithm greedily walks the graph, maintaining a priority queue of the `svs_search_window_size` closest candidates seen so far. At each hop, the closest unvisited candidate is explored next; the search ends once every neighbor of the current node is farther from the query than the worst candidate still in the queue. A larger `svs_search_window_size` explores more of the graph, improving recall at the cost of latency.

### LeanVec compression

[LeanVec](https://openreview.net/forum?id=wczqrpOrIc) is a compression technique that reduces the dimensionality of vectors and the bits used per dimension. When LeanVec is enabled (`index_type: "SVS_VAMANA_LEANVEC"`), SVS keeps two representations of each vector:

- **Primary (reduced-dimensionality)**: A linear projection of the vector down to `svs_leanvec_dim` dimensions. The Vamana graph search runs over this primary dataset, so most distance computations happen in the lower-dimensional space, which reduces both compute and memory-bandwidth requirements. If `svs_leanvec_dim` is left at its default of `0`, the reduced dimensionality defaults to half the original dimensionality (`dim / 2`).

- **Secondary (full-dimensionality)**: A version of the vector at full dimensionality. Candidates returned by the primary graph search are re-ranked using this secondary dataset to recover accuracy lost to dimensionality reduction.

Both representations can be quantized with [LVQ](https://vldb.org/pvldb/volumes/16/paper/Similarity%20search%20in%20the%20blink%20of%20an%20eye%20with%20compressed%20indices). The `svs_storage_kind` parameter selects the LVQ encoding used — for example, `leanvec4x8` uses 4 bits per dimension for the primary encoding and 8 bits per dimension for the secondary encoding.

By default, LeanVec performs dimensionality reduction with a method that supports queries that do not follow the same data distribution as the indexed vectors (out-of-distribution, OOD). This works particularly well for cross-modal workloads such as text-to-image retrieval, where query vectors have a different modality than the indexed vectors. It also works well for most cases where the queries are not OOD. However, if you want to sacrifice some query performance to speed up indexing, turn off OOD support by setting `svs_leanvec_ood: false`.

### LVQ compression

For low dimensional datasets (<512), it may be preferable to skip LeanVec dimensionality reduction and compress the data only using LVQ quantization. Similar to LeanVec, `SVS_VAMANA_LVQ` indexes keep two representations for each vector: a primary representation for fast searching and a residual representation for reranking search results. For example, `lvq4x4` uses 4 bits for the primary representation and 4 bits for the residual representation. LVQ also supports skipping the reranking, e.g., `lvq4x0` to speed up queries if recall is acceptable.

<div class="alert note">

LVQ and LeanVec compression only run on Intel CPUs. The other storage kinds (<code>fp32</code>, <code>fp16</code>, <code>sqi8</code>) used by the base <code>SVS_VAMANA</code> index do not have this requirement.

</div>

## Build index

To build an `SVS_VAMANA` index on a vector field in Milvus, use the `add_index()` method, specifying the `index_type`, `metric_type`, and additional parameters for the index.

```python
from pymilvus import MilvusClient

# Prepare index building params
index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name="your_vector_field_name", # Name of the vector field to be indexed
    index_type="SVS_VAMANA", # Type of the index to create
    index_name="vector_index", # Name of the index to create
    metric_type="L2", # Metric type used to measure similarity
    params={
        "svs_graph_max_degree": 64, # Maximum number of edges per node in the Vamana graph
        "svs_construction_window_size": 200, # Candidate list size used while building the graph
        "svs_storage_kind": "fp32", # Storage format for the indexed vectors
    } # Index building params
)
```

In this configuration:

- `index_type`: The type of index to be built. In this example, set the value to `SVS_VAMANA`.

- `metric_type`: The method used to calculate the distance between vectors. Supported values include `COSINE`, `L2`, and `IP`. For details, refer to [Metric Types](metric.md).

- `params`: Additional configuration options for building the index.

    - `svs_graph_max_degree`: Maximum number of edges each node can have in the Vamana graph.

    - `svs_construction_window_size`: Size of the candidate list explored for each node during graph construction.

    - `svs_storage_kind`: Storage format used for the indexed vectors.

    To learn more building parameters available for the `SVS_VAMANA` index, refer to [Index building params](svs-vamana.md#Index-building-params).

To enable LeanVec compression, set `index_type` to `SVS_VAMANA_LEANVEC` and use a `leanvec*` storage kind:

```python
index_params.add_index(
    field_name="your_vector_field_name", # Name of the vector field to be indexed
    index_type="SVS_VAMANA_LEANVEC", # Type of the index to create
    index_name="vector_index", # Name of the index to create
    metric_type="L2", # Metric type used to measure similarity
    params={
        "svs_graph_max_degree": 64, # Maximum number of edges per node in the Vamana graph
        "svs_construction_window_size": 200, # Candidate list size used while building the graph
        "svs_storage_kind": "leanvec4x8", # LeanVec encoding for the primary and secondary datasets
    } # Index building params
)
```

To learn more about the LeanVec-specific parameters, refer to [LeanVec params](svs-vamana.md#LeanVec-params).

Once the index parameters are configured, you can create the index by using the `create_index()` method directly or passing the index params in the `create_collection` method. For details, refer to [Create Collection](create-collection.md).

## Search on index

Once the index is built and entities are inserted, you can perform similarity searches on the index.

```python
search_params = {
    "params": {
        "svs_search_window_size": 100, # Candidate list size explored during search
    }
}

res = MilvusClient.search(
    collection_name="your_collection_name", # Collection name
    anns_field="vector_field", # Vector field name
    data=[[0.1, 0.2, 0.3, 0.4, 0.5]],  # Query vector
    limit=10,  # TopK results to return
    search_params=search_params
)
```

In this configuration:

- `params`: Additional configuration options for searching on the index.

    - `svs_search_window_size`: Size of the candidate list maintained while traversing the graph.

    To learn more search parameters available for the `SVS_VAMANA` index, refer to [Index-specific search params](svs-vamana.md#Index-specific-search-params).

The same search parameters apply when searching an `SVS_VAMANA_LEANVEC` index.

## Index params

This section provides an overview of the parameters used for building an index and performing searches on the index.

### Index building params

The following table lists the parameters that can be configured in `params` when [building an index](svs-vamana.md#Build-index).

<table>
   <tr>
     <th><p>Parameter</p></th>
     <th><p>Description</p></th>
     <th><p>Value Range</p></th>
     <th><p>Tuning Suggestion</p></th>
   </tr>
   <tr>
     <td><p><code>svs_graph_max_degree</code></p></td>
     <td><p>Maximum number of edges (connections) each node can have in the Vamana graph.</p></td>
     <td><p><strong>Type</strong>: Integer</p><p><strong>Range</strong>: [4, 256]</p><p><strong>Default value</strong>: <code>32</code> (<code>64</code> for <code>SVS_VAMANA_LEANVEC</code>)</p></td>
     <td><p>Higher values create denser graphs, potentially increasing recall but also increasing memory usage and build time. In most cases, we recommend you set a value within this range: [32, 128].</p></td>
   </tr>
   <tr>
     <td><p><code>svs_construction_window_size</code></p></td>
     <td><p>Size of the candidate list maintained while searching for neighbors of each node during graph construction.</p></td>
     <td><p><strong>Type</strong>: Integer</p><p><strong>Range</strong>: [1, 10000]</p><p><strong>Default value</strong>: <code>128</code></p></td>
     <td><p>Larger values improve graph quality and search accuracy at the cost of longer build time. It should generally be set to a value greater than or equal to <code>svs_graph_max_degree</code>.</p></td>
   </tr>
   <tr>
     <td><p><code>svs_alpha</code></p></td>
     <td><p>Pruning parameter used during graph construction. Larger values favor longer-range edges over redundant short-range ones.</p></td>
     <td><p><strong>Type</strong>: Float</p><p><strong>Range</strong>: [0.0, 10.0]</p><p><strong>Default value</strong>: <code>1.2</code> for <code>L2</code>, <code>0.95</code> for <code>IP</code>/<code>COSINE</code></p></td>
     <td><p>Use the metric-dependent default unless you have measured a better value for your dataset: values above 1 are appropriate for metrics that minimize (<code>L2</code>), values below 1 for metrics that maximize (<code>IP</code>, <code>COSINE</code>).</p></td>
   </tr>
   <tr>
     <td><p><code>svs_storage_kind</code></p></td>
     <td><p>Storage format used for the indexed vectors.</p></td>
     <td><p><strong>Type</strong>: String</p><p><strong>Range</strong>: [<code>fp32</code>, <code>fp16</code>, <code>sqi8</code>] for <code>SVS_VAMANA</code>; [<code>lvq4x0</code>, <code>lvq4x4</code>, <code>lvq4x8</code>] for <code>SVS_VAMANA_LVQ</code>; [<code>leanvec4x4</code>, <code>leanvec4x8</code>, <code>leanvec8x8</code>] for <code>SVS_VAMANA_LEANVEC</code></p><p><strong>Default value</strong>: <code>fp32</code> (<code>lvq4x4</code> / <code>leanvec4x4</code> for the LVQ / LeanVec index types)</p></td>
     <td><p><code>fp16</code> and <code>sqi8</code> reduce memory usage relative to <code>fp32</code> with minimal accuracy loss. The <code>lvq*</code> and <code>leanvec*</code> kinds compress further; higher numbers (e.g., <code>lvq4x8</code> over <code>lvq4x0</code>) trade off memory saving for higher accuracy.</p></td>
   </tr>
</table>

### Index-specific search params

The following table lists the parameters that can be configured in `search_params.params` when [searching on the index](svs-vamana.md#Search-on-index).

<table>
   <tr>
     <th><p>Parameter</p></th>
     <th><p>Description</p></th>
     <th><p>Value Range</p></th>
     <th><p>Tuning Suggestion</p></th>
   </tr>
   <tr>
     <td><p><code>svs_search_window_size</code></p></td>
     <td><p>Size of the candidate list maintained while traversing the graph during a search.</p></td>
     <td><p><strong>Type</strong>: Integer</p><p><strong>Range</strong>: [1, 10000]</p><p><strong>Default value</strong>: <code>64</code></p></td>
     <td><p>Larger values increase the chances of finding the true nearest neighbors (higher recall) but also increase search latency. It should be set to a value at least as large as the desired number of results.</p></td>
   </tr>
   <tr>
     <td><p><code>svs_search_buffer_capacity</code></p></td>
     <td><p>Capacity of the priority queue used to track the best candidates seen so far during a search.</p></td>
     <td><p><strong>Type</strong>: Integer</p><p><strong>Range</strong>: [1, 10000]</p><p><strong>Default value</strong>: <code>64</code></p></td>
     <td><p>In most cases, we recommend setting this equal to <code>svs_search_window_size</code>. For <code>SVS_VAMANA_LEANVEC</code>, set it to 1.5x <code>svs_search_window_size</code></p></td>
   </tr>
</table>

### LeanVec params

The following table lists the additional parameters available in `params` when building an [`SVS_VAMANA_LEANVEC`](svs-vamana.md#Build-index) index.

<table>
   <tr>
     <th><p>Parameter</p></th>
     <th><p>Description</p></th>
     <th><p>Value Range</p></th>
     <th><p>Tuning Suggestion</p></th>
   </tr>
   <tr>
     <td><p><code>svs_leanvec_dim</code></p></td>
     <td><p>Reduced dimensionality of the primary dataset used for graph search.</p></td>
     <td><p><strong>Type</strong>: Integer</p><p><strong>Range</strong>: [0, 65536]</p><p><strong>Default value</strong>: <code>0</code> (uses <code>dim / 2</code>)</p></td>
     <td><p>Smaller values reduce memory usage and speed up graph search but increase the accuracy lost to dimensionality reduction, which the secondary dataset must recover during re-ranking. The default of half the original dimensionality is a reasonable starting point.</p></td>
   </tr>
   <tr>
     <td><p><code>svs_leanvec_ood</code></p></td>
     <td><p>Whether to the out-of-distribution (OOD) method for dimensionality reduction..</p></td>
     <td><p><strong>Type</strong>: Boolean</p><p><strong>Range</strong>: [<code>true</code>, <code>false</code>]</p><p><strong>Default value</strong>: <code>true</code></p></td>
     <td><p>Default works in most cases, including when queries are from the same distribution as the database vectors. Set to <code>false</code> only when indexing time is more important than query performance.</p></td>
   </tr>
</table>
