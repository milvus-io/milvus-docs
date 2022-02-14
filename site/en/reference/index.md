---
id: index.md
related_key: index
summary: Index mechanism in Milvus.
---

# Vector Index

Indexing, a process of organizing data, is a huge component of what makes it possible to efficiently query the million-, billion-, or even trillion-vector datasets that vector databases rely on. 

## Accelerating vector similarity search

Similarity search engines work by comparing an input to the objects in a database to find those that are most similar to the input. Indexing is the process of efficiently organizing data, and it plays a major role in making similarity search useful by dramatically accelerating time-consuming queries on large datasets. After a massive vector dataset is indexed, queries can be routed to clusters, or subsets of data, that are most likely to contain vectors similar to an input query. In practice, this means a certain degree of accuracy is sacrificed to speed up queries on really large vector datasets.

To improve query performance, you can specify an index type for each vector field. Currently, a vector field only supports one index type. Milvus automatically deletes the old index when switching the index type.

## Create indexes

When the `create_index` method is called, Milvus synchronously indexes the existing data on vector field. Whereas Milvus stores massive data in segments, it creates an index file for each data segment separately when indexing.

<div class="alert note">
By default, Milvus does not index a segment with less than 1,024 rows. To change this parameter, configure <a href="configure_rootcoord.md#rootCoord.minSegmentSizeToEnableIndex"><code>rootCoord.minSegmentSizeToEnableIndex</code></a> in <code>milvus.yaml</code>.
</div>


## Selecting an Index Best Suited for Your Scenario

Most of the vector index types supported by Milvus use approximate nearest neighbors search (ANNS). Compared with accurate retrieval, which is usually very time-consuming, the core idea of ANNS is no longer limited to returning the most accurate result, but only searching for neighbors of the target. ANNS improves retrieval efficiency by sacrificing accuracy within an acceptable range.

To learn how to choose an appropriate metric for an index, see [Similarity Metrics](metric.md).

According to the implementation methods, the ANNS vector index can be divided into four categories:

- Tree-based index
- Graph-based index
- Hash-based index
- Quantization-based index

The following table classifies the indexes that Milvus supports:

<table>
<thead>
  <tr>
    <th>Supported index</th>
    <th>Classification</th>
    <th>Scenario</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><a href="#FLAT">FLAT</a></td>
    <td>N/A</td>
    <td>
      <ul>
        <li>Relatively small dataset</li>
        <li>Requires a 100% recall rate</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><a href="#IVF_FLAT">IVF_FLAT</a></td>
    <td>Quantization-based index</td>
    <td>
      <ul>
        <li>High-speed query</li>
        <li>Requires a recall rate as high as possible</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><a href="#IVF_SQ8">IVF_SQ8</a></td>
    <td>Quantization-based index</td>
    <td>
      <ul>
        <li>High-speed query</li>
        <li>Limited memory resources</li>
        <li>Accepts minor compromise in recall rate</li>
      </ul>
    </td>
  </tr>  
  <tr>
    <td><a href="#IVF_PQ">IVF_PQ</a></td>
    <td>Quantization-based index</td>
    <td>
      <ul>
        <li>Very high-speed query</li>
        <li>Limited memory resources</li>
        <li>Accepts substantial compromise in recall rate</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><a href="#HNSW">HNSW</a></td>
    <td>Graph-based index</td>
    <td>
      <ul>
        <li>High-speed query</li>
        <li>Requires a recall rate as high as possible</li>
        <li>Large memory resources</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><a href="#IVF_HNSW">IVF_HNSW</a></td>
    <td>Quantization-and-graph-based index</td>
    <td>
      <ul>
        <li>High-speed query</li>
        <li>Requires a recall rate as high as possible</li>
        <li>Large memory resources</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><a href="#RHNSW_FLAT">RHNSW_FLAT</a></td>
    <td>Quantization-and-graph-based index</td>
    <td>
      <ul>
        <li>High-speed query</li>
        <li>Requires a recall rate as high as possible</li>
        <li>Large memory resources</li>
      </ul>
    </td>
  <tr>
    <td><a href="#RHNSW_SQ">RHNSW_SQ</a></td>
    <td>Quantization-and-graph-based index</td>
    <td>
      <ul>
        <li>High-speed query</li>
        <li>Limited memory resources</li>
        <li>Accepts minor compromise in recall rate</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><a href="#RHNSW_PQ">RHNSW_PQ</a></td>
    <td>Quantization-and-graph-based index</td>
    <td>
      <ul>
        <li>Very high-speed query</li>
        <li>Limited memory resources</li>
        <li>Accepts substantial compromise in recall rate</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><a href="#ANNOY">ANNOY</a></td>
    <td>Tree-based index</td>
    <td>
      <ul>
        <li>Low-dimensional vectors</li>
      </ul>
    </td>
  </tr>
</tbody>
</table>



### Supported vector indexes

#### FLAT

<a name="FLAT"></a>

For vector similarity search applications that require perfect accuracy and depend on relatively small (million-scale) datasets, the FLAT index is a good choice. FLAT does not compress vectors, and is the only index that can guarantee exact search results. Results from FLAT can also be used as a point of comparison for results produced by other indexes that have less than 100% recall.

FLAT is accurate because it takes an exhaustive approach to search, which means for each query the target input is compared to every vector in a dataset. This makes FLAT the slowest index on our list, and poorly suited for querying massive vector data. There are no parameters for the FLAT index in Milvus, and using it does not require data training or additional storage.

- Search parameters

  | Parameter     | Description                            | Range                               |
  | ------------- | -------------------------------------- | ----------------------------------- |
  | `metric_type` | [Optional] The chosen distance metric. | See [Supported Metrics](metric.md). |

#### IVF_FLAT

<a name="IVF_FLAT"></a>

IVF_FLAT divides vector data into `nlist` cluster units, and then compares distances between the target input vector and the center of each cluster. Depending on the number of clusters the system is set to query (`nprobe`), similarity search results are returned based on comparisons between the target input and the vectors in the most similar cluster(s) only — drastically reducing query time.

By adjusting `nprobe`, an ideal balance between accuracy and speed can be found for a given scenario. Results from the [IVF_FLAT performance test](https://zilliz.com/blog/Accelerating-Similarity-Search-on-Really-Big-Data-with-Vector-Indexing) demonstrate that query time increases sharply as both the number of target input vectors (`nq`), and the number of clusters to search (`nprobe`), increase.

IVF_FLAT is the most basic IVF index, and the encoded data stored in each unit is consistent with the original data.

 - Index building parameters

   | Parameter | Description             | Range      |
   | --------- | ----------------------- | ---------- |
   | `nlist`   | Number of cluster units | [1, 65536] |


- Search parameters

  | Parameter | Description              | Range                                           |
  | --------- | ------------------------ | ----------------------------------------------- |
  | `nprobe`  | Number of units to query | CPU: [1, nlist] <br> GPU: [1, min(2048, nlist)] |

#### IVF_SQ8

<a name="IVF_SQ8"></a>

IVF_FLAT does not perform any compression, so the index files it produces are roughly the same size as the original, raw non-indexed vector data. For example, if the original 1B SIFT dataset is 476 GB, its IVF_FLAT index files will be slightly larger (~470 GB). Loading all the index files into memory will consume 470 GB of storage.

When disk, CPU, or GPU memory resources are limited, IVF_SQ8 is a better option than IVF_FLAT. This index type can convert each FLOAT (4 bytes) to UINT8 (1 byte) by performing scalar quantization. This reduces disk, CPU, and GPU memory consumption by 70–75%. For the 1B SIFT dataset, the IVF_SQ8 index files require just 140 GB of storage.


 - Index building parameters

   | Parameter | Description             | Range      |
   | --------- | ----------------------- | ---------- |
   | `nlist`   | Number of cluster units | [1, 65536] |


- Search parameters

  | Parameter | Description              | Range                                           |
  | --------- | ------------------------ | ----------------------------------------------- |
  | `nprobe`  | Number of units to query | CPU: [1, nlist] <br> GPU: [1, min(2048, nlist)] |

#### IVF_PQ

<a name="IVF_PQ"></a>

`PQ` (Product Quantization) uniformly decomposes the original high-dimensional vector space into Cartesian products of `m` low-dimensional vector spaces, and then quantizes the decomposed low-dimensional vector spaces. Instead of calculating the distances between the target vector and the center of all the units, product quantization enables the calculation of distances between the target vector and the clustering center of each low-dimensional space and greatly reduces the time complexity and space complexity of the algorithm.

IVF\_PQ performs IVF index clustering before quantizing the product of vectors. Its index file is even smaller than IVF\_SQ8, but it also causes a loss of accuracy during searching vectors.

<div class="alert note">
Index building parameters and search parameters vary with Milvus distribution. Select your Milvus distribution first.
</div>

- Index building parameters

  | Parameter | Description                               | Range               |
  | --------- | ----------------------------------------- | ------------------- |
  | `nlist`   | Number of cluster units                   | [1, 65536]          |
  | `m`       | Number of factors of product quantization | `dim` ≡ 0 (mod `m`) |
  | `nbits`   | [Optional] Number of bits in which each low-dimensional vector is stored. | [1, 16] (8 by default) |

- Search parameters

  | Parameter | Description              | Range      |
  | --------- | ------------------------ | ---------- |
  | `nprobe`  | Number of units to query | [1, nlist] |



#### HNSW

<a name="HNSW"></a>

HNSW (Hierarchical Navigable Small World Graph) is a graph-based indexing algorithm. It builds a multi-layer navigation structure for an image according to certain rules. In this structure, the upper layers are more sparse and the distances between nodes are farther; the lower layers are denser and the distances between nodes are closer. The search starts from the uppermost layer, finds the node closest to the target in this layer, and then enters the next layer to begin another search. After multiple iterations, it can quickly approach the target position.

In order to improve performance, HNSW limits the maximum degree of nodes on each layer of the graph to `M`. In addition, you can use `efConstruction` (when building index) or `ef` (when searching targets) to specify a search range.

- Index building parameters

  | Parameter        | Description                | Range    |
  | ---------------- | -------------------------- | -------- |
  | `M`              | Maximum degree of the node | [4, 64]  |
  | `efConstruction` | Search scope               | [8, 512] |


- Search parameters

  | Parameter | Description  | Range            |
  | --------- | ------------ | ---------------- |
  | `ef`      | Search scope | [`top_k`, 32768] |

#### IVF_HNSW

<a name="IVF_HNSW"></a>

IVF_HNSW is an indexing algorithm based on IVF_FLAT and HNSW. Using HNSW indexing algorithm as quantizer, this index type builds the multi-layer navigation structure with the `nlist` cluster units divided by IVF_FLAT indexing algorithm, so that it can approach the target position quickly.


- Index building parameters

  | Parameter        | Description                | Range      |
  | ---------------- | -------------------------- | ---------- |
  | `nlist`          | Number of cluster units    | [1, 65536] |
  | `M`              | Maximum degree of the node | [4, 64]    |
  | `efConstruction` | Search scope               | [8, 512]   |

- Search parameters

  | Parameter | Description                | Range            |
  | --------- | -------------------------- | ---------------- |
  | `nprobe`  | Number of units to query   | [1, nlist]       |
  | `ef`      | Search scope               | [`top_k`, 32768] |

#### RHNSW_FLAT

<a name="RHNSW_FLAT"></a>

RHNSW_FLAT (Refined Hierarchical Small World Graph) is a refined indexing algorithm based on HNSW. This index type optimizes the data storage solution of HNSW and thereby reduces the storage consumption.

- Index building parameters

  | Parameter        | Description                | Range    |
  | ---------------- | -------------------------- | -------- |
  | `M`              | Maximum degree of the node | [4, 64]  |
  | `efConstruction` | Search scope               | [8, 512] |


- Search parameters

  | Parameter | Description  | Range            |
  | --------- | ------------ | ---------------- |
  | `ef`      | Search scope | [`top_k`, 32768] |

#### RHNSW_SQ

<a name="RHNSW_SQ"></a>

RHNSW_SQ (Refined Hierarchical Small World Graph and Scalar Quantization) is a refined indexing algorithm based on HNSW. This index type performs scalar quantization on vector data on the basis of HNSW and thereby substantially reduces the storage consumption.

- Index building parameters

  | Parameter        | Description                | Range    |
  | ---------------- | -------------------------- | -------- |
  | `M`              | Maximum degree of the node | [4, 64]  |
  | `efConstruction` | Search scope               | [8, 512] |


- Search parameters

  | Parameter | Description  | Range            |
  | --------- | ------------ | ---------------- |
  | `ef`      | Search scope | [`top_k`, 32768] |

#### RHNSW_PQ

<a name="RHNSW_PQ"></a>

RHNSW_SQ (Refined Hierarchical Small World Graph and Product Quantization) is a refined indexing algorithm based on HNSW. This index type performs product quantization on vector data on the basis of HNSW and thereby significantly reduces the storage consumption.

- Index building parameters

  | Parameter        | Description                               | Range               |
  | ---------------- | ----------------------------------------- | ------------------- |
  | `M`              | Maximum degree of the node                | [4, 64]             |
  | `efConstruction` | Search scope                              | [8, 512]            |
  | `PQM`            | Number of factors of product quantization | dim ≡ 0 (mod `PQM`) |


- Search parameters

  | Parameter | Description  | Range            |
  | --------- | ------------ | ---------------- |
  | `ef`      | Search scope | [`top_k`, 32768] |

#### ANNOY

<a name="ANNOY"></a>

ANNOY (Approximate Nearest Neighbors Oh Yeah) is an index that uses a hyperplane to divide a high-dimensional space into multiple subspaces, and then stores them in a tree structure.

When searching for vectors, ANNOY follows the tree structure to find subspaces closer to the target vector, and then compares all the vectors in these subspaces (The number of vectors being compared should not be less than `search_k`) to obtain the final result. Obviously, when the target vector is close to the edge of a certain subspace, sometimes it is necessary to greatly increase the number of searched subspaces to obtain a high recall rate. Therefore, ANNOY uses `n_trees` different methods to divide the whole space, and searches all the dividing methods simultaneously to reduce the probability that the target vector is always at the edge of the subspace.


- Index building parameters

  | Parameter | Description                              | Range     |
  | --------- | ---------------------------------------- | --------- |
  | `n_trees` | The number of methods of space division. | [1, 1024] |

- Search parameters

  | Parameter  | Description                                                  | Range                           |
  | ---------- | ------------------------------------------------------------ | ------------------------------- |
  | `search_k` | The number of nodes to search. -1 means 5% of the whole data. | {-1} ∪ [`top_k`, n × `n_trees`] |



## FAQ


<details>
<summary><font color="#4fc4f9">What is the difference between FLAT index and IVF_FLAT index?</font></summary>
{{fragments/faq_flat_ivfflat.md}}
</details>


## Bibliography

- HNSW: <a href="https://arxiv.org/abs/1603.09320">Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs</a>
- ANNOY: <a href="https://erikbern.com/2015/10/01/nearest-neighbors-and-vector-models-part-2-how-to-search-in-high-dimensional-spaces.html">Nearest neighbors and vector models – part 2 – algorithms and data structures</a>

