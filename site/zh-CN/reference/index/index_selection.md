---
id: index_selection.md
related_key: IVF
---

# 根据应用场景选择索引

{{fragments/translation_needed.md}}

Milvus 目前支持的向量索引类型大都属于 ANNS（Approximate Nearest Neighbors Search，近似最近邻搜索）。ANNS 的核心思想是不再局限于只返回最精确的结果项，而是仅搜索可能是近邻的数据项，即以牺牲可接受范围内的精度的方式提高检索效率。

根据实现方式，ANNS 向量索引可分为四大类：

- 基于树的索引

- 基于图的索引

- 基于哈希的索引

- 基于量化的索引

下表将目前 Milvus 支持的索引进行了归类：

<table>
<thead>
  <tr>
    <th>Milvus 支持的索引</th>
    <th>索引分类</th>
    <th>适用场景</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><a href="#FLAT">FLAT</a></td>
    <td>N/A</td>
    <td><ul>
        <li>查询数据规模小</li>
        <li>需要 100% 的召回率。</li>
        </ul></td>
  </tr>
  <tr>
    <td><a href="#IVF_FLAT">IVF_FLAT</a></td>
    <td>基于量化的索引</td>
    <td><ul>
        <li>高速查询</li>
        <li>要求高召回率</li>
        </ul></td>
  </tr>
  <tr>
    <td><a href="#IVF_SQ8">IVF_SQ8</a></td>
    <td>基于量化的索引</td>
    <td><ul>
        <li>高速查询</li>
        <li>磁盘和内存资源有限</li>
        <li>查询召回率低于 IVF_FLAT</li>
        </ul></td>
  </tr>
  <tr>
    <td><a href="#IVF_PQ">IVF_PQ</a></td>
    <td>基于量化的索引</td>
    <td><ul>
        <li>超高速查询</li>
        <li>磁盘和内存资源有限</li>
        <li>可以接受偏低的查询召回率</li>
        </ul></td>
  </tr>
  <tr>
    <td><a href="#HNSW">HNSW</a></td>
    <td>基于图的索引</td>
    <td><ul>
        <li>高速查询</li>
        <li>要求尽可能高的召回率</li>
        <li>内存空间大</li>
        </ul></td>
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
    <td>基于树的索引</td>
    <td><ul>
        <li>低维向量空间</li>
        </ul></td>
  </tr>
</tbody>
</table>

## 索引概览

### FLAT

<a name="FLAT"></a>

对于需要 100% 召回率且数据规模相对较小（百万级）的向量相似性搜索应用，FLAT 索引是一个很好的选择。FLAT 是指对向量进行原始文件存储，是唯一可以保证精确的检索结果的索引。FLAT 的结果也可以用于对照其他召回率低于 100% 的索引产生的结果。

FLAT 之所以精准是因为它采取了详尽查询的方法，即对于每个查询，目标输入都要与数据集中的每个向量进行比较。因此 FLAT 是列表中查询速度最慢的，而且不适合查询大量的向量数据。Milvus 中没有 FLAT 索引的参数，使用它不需要数据训练，也不需要占用额外的磁盘空间。

- 查询参数

  | 参数          | 说明                | 取值范围                                   |
  | ------------- | ------------------- | ------------------------------------------ |
  | `metric_type` | [可选] 距离计算方式 | 详见 [目前支持的距离计算方式](metric.md)。 |

### IVF_FLAT

<a name="IVF_FLAT"></a>​

IVF_FLAT 它通过聚类方法把空间里的点划分至 `nlist` 个单元，然后比较目标向量与所有单元中心的距离，选出 `nprobe` 个最近单元。然后比较这些被选中单元里的所有向量，得到最终的结果，极大地缩短了查询时间。 

通过调整 `nprobe`，可以找到特定场景下查询准确性和查询速度之间的理想平衡。IVF_FLAT 性能测试结果表明，随着目标输入向量的数量（`nq`）和需要检索的集群数量（`nprobe`）的增加，查询时间也急剧增加。

IVF_FLAT 是最基础的 IVF 索引，存储在各个单元中的数据编码与原始数据一致。

- 建索引参数

   | 参数   | 说明     | 取值范围     |
   | ------- | -------- |----------- |
   | `nlist` | 聚类单元数 |[1, 65536] |
   

- 查询参数

   | 参数     | 说明        | 取值范围    |
   | -------- | ----------- | ---------- |
   | `nprobe` | 查询取的单元数 | [1, 65536] |

### IVF_SQ8

<a name="IVF_SQ8"></a>​

由于 IVF_FLAT 未对原始的向量数据做任何压缩，IVF_FLAT 索引文件的大小与原始数据文件大小相当。例如 sift-1b 数据集原始数据文件的大小为 476 GB，生成的 IVF_FLAT 索引文件大小有 470 GB 左右，若将全部索引文件加载进内存，就需要 470 GB 的内存资源。

当磁盘或内存、显存资源有限时，IVF_SQ8 是一个更好的选择。它通过对向量进行标量量化（scalar quantization），能把原始向量中每个FLOAT（4 字节）转为UINT8（1 字节），从而可以把磁盘及内存、显存资源的消耗量减少为原来的 1/4 至 1/3。同样以 sift-1b 数据集为例，生成的 IVF_SQ8 索引文件只有 140 GB。

- 建索引参数

   | 参数   | 说明     | 取值范围     |
   | ------- | -------- |----------- |
   | `nlist` | 聚类单元数 |[1, 65536] |
   

- 查询参数

   | 参数     | 说明        | 取值范围    |
   | -------- | ----------- | ---------- |
   | `nprobe` | 查询取的单元数 | [1, nlist] |
   
### IVF_PQ

<a name="IVF_PQ"></a>

`PQ`（Product Quantization，乘积量化）会将原来的高维向量空间均匀分解成 `m` 个低维向量空间的笛卡尔积，然后对分解得到的低维向量空间分别做矢量量化。最终每条向量会存储在 `m` × `nbits` 个 bit 位里。乘积量化能将全样本的距离计算转化为到各低维空间聚类中心的距离计算，从而大大降低算法的时间复杂度。

IVF_PQ 是先对向量做乘积量化，然后进行 IVF 索引聚类。其索引文件甚至可以比 IVF_SQ8 更小，不过同样地也会导致查询时的精度损失。

<div class="alert note">

不同版本的建索引参数和查询参数设置不同，请根据使用的 Milvus 版本查看相应的参数信息。

</div>

- 建索引参数

   | 参数   | 说明          | 取值范围     |
   | --------| ------------- | ----------- |
   | `nlist` | 聚类单元数　    | [1, 65536] |
   | `m`     | 乘积量化因子个数 | dim ≡ 0 (mod m) |
   | `nbits` | 分解后每个低维向量的存储位数 (可选) | [1, 16]（默认 8）|

- 查询参数

   | 参数   | 说明          | 取值范围     |
   | -------- | ----------- | ---------- |
   | `nprobe` | 查询取的单元数 | [1, nlist] |


### HNSW
<a name="HNSW"></a>

HNSW（Hierarchical Small World Graph）是一种基于图的索引算法。它会为一张图按规则建成多层导航图，并让越上层的图越稀疏，结点间的距离越远；越下层的图越稠密，结点间的距离越近。搜索时从最上层开始，找到本层距离目标最近的结点后进入下一层再查找。如此迭代，快速逼近目标位置。
  
为了提高性能，HNSW 限定了每层图上结点的最大度数 `M` 。此外，建索引时可以用 `efConstruction`，查询时可以用 `ef` 来指定搜索范围。



- 建索引参数

   | 参数            | 说明                | 取值范围   |
   | ---------------- | ------------------ | --------- |
   | `M`              | 结点的最大度数        | [4, 64]  |
   | `efConstruction` | 搜索范围      | [8, 512] |

- 查询参数

   | 参数   | 说明            | 取值范围      |
   | --------|--------------- | ------------ |
   | `ef`    | 搜索范围  | [`top_k`, 32768] |

### IVF_HNSW

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

### RHNSW_FLAT

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

### RHNSW_SQ

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

### RHNSW_PQ

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


### Annoy
<a name="Annoy"></a>

Annoy（Approximate Nearest Neighbors Oh Yeah）是一种用超平面把高维空间分割成多个子空间，并把这些子空间以树型结构存储的索引方式。

在查询时，Annoy 会顺着树结构找到距离目标向量较近的一些子空间，然后比较这些子空间里的所有向量（要求比较的向量数不少于 `search_k` 个）以获得最终结果。显然，当目标向量靠近某个子空间的边缘时，有时需要大大增加搜索的子空间数以获得高召回率。因此，Annoy 会使用 `n_trees` 次不同的方法来划分全空间，并同时搜索所有划分方法以减少目标向量总是处于子空间边缘的概率。

- 建索引参数

   | 参数     | 说明     　    | 取值范围  |
   | --------- |-------------- | -------- |
   | `n_trees` | 空间划分的方法数 | [1, 1024] |

- 查询参数

   | 参数      | 说明                              | 取值范围          |
   | -----------|--------------------------------- | ---------------- |
   | `search_k` | 搜索的结点数。`-1` 表示用全数据量的 5% | {-1} ∪ [`top_k`, n × `n_trees`] |
   
## 常见问题

<details>
<summary><font color="#4fc4f9">Milvus 中 FLAT 索引和 IVF_FLAT 索引的原理比较？</font></summary>
{{fragments/faq_flat_ivfflat.md}}
</details>

## 参考文献

- HNSW：<a href="https://arxiv.org/abs/1603.09320">Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs</a>
- Annoy：<a href="https://erikbern.com/2015/10/01/nearest-neighbors-and-vector-models-part-2-how-to-search-in-high-dimensional-spaces.html">Nearest neighbors and vector models – part 2 – algorithms and data structures</a>
