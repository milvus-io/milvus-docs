---
id: metric-binary.md
label: 二值型向量
order: 1
group: vector
---
{{fragments/metrics.md}}

{{tab}} 

<<<<<<< HEAD:site/zh-CN/milvus_basics/metric-binary.md
<div class="filter-binary table-wrapper" markdown="block">
=======
>>>>>>> a8c4ae2dbd71bf35881a051610ad23772111eda9:site/zh-CN/milvus_basics/metric.md

<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky">距离计算方式</th>
    <th class="tg-0pky">索引类型</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky">杰卡德距离 (Jaccard)<br>谷本距离 (Tanimoto)<br>汉明距离 (Hamming)</td>
    <td class="tg-0pky"><ul><li>FLAT</li><li>IVF_FLAT</li></ul></td>
  </tr>
  <tr>
    <td class="tg-0pky">超结构 (superstructure)<br>子结构 (substructure)</td>
    <td class="tg-0pky">FLAT</td>
  </tr>
</tbody>
</table>

<<<<<<< HEAD:site/zh-CN/milvus_basics/metric-binary.md

<div class="filter-binary" markdown="block">
=======
>>>>>>> a8c4ae2dbd71bf35881a051610ad23772111eda9:site/zh-CN/milvus_basics/metric.md

### 杰卡德距离

杰卡德相似系数计算数据集之间的相似度，计算方式为：数据集交集的个数和并集个数的比值。计算公式可以表示为：

![Jaccard similarity coefficient](../../../assets/jaccard_coeff.png)

杰卡德距离是用来衡量两个数据集差异性的一种指标，被定义为 1 减去杰卡德相似系数。对于二值变量，杰卡德距离等价于谷本系数。

![Jaccard distance](../../../assets/jaccard_dist.png)

杰卡德距离适合字符串相似性度量。

### 谷本距离

对于二值变量，谷本距离公式可表示为：

![tanimoto distance](../../../assets/tanimoto_dist.png)

在 Milvus 中，谷本距离仅支持二值变量。

值域从 0 到正无穷。

对于二值变量，谷本系数等价于杰卡德距离：

![tanimoto coefficient](../../../assets/tanimoto_coeff.png)

对于二值变量，谷本系数值域为 0 到 +1（+1 的相似度最高）

### 汉明距离

汉明距离计算二进制字符串之间的距离。两个等长字符串之间的汉明距离定义为将其中一个变为另外一个所需要作的最小替换次数。

比如，假设有两条字符串 1101 1001 和 1001 1101。比较时，如果字符相同用 0 表示，如果字符不同则用 1 表示。

11011001 ⊕ 10011101 = 01000100

所以以上两条字符串之间的汉明距离为 2。

### 超结构

超结构主要用来计算某化学结构与其超结构的相似度。值越小则相似度越大。Milvus 目前只返回距离为 0 的结果。

超结构的公式可表示为：

![superstructure](../../../assets/superstructure.png)

其中

- 分子式 B 是分子式 A 的超结构。
- N<sub>A</sub> 表示分子式 A 的化学指纹中二进制位的数量。
- N<sub>B</sub> 表示分子式 B 的化学指纹中二进制位的数量。
- N<sub>AB</sub> 表示分子式 A 和 B 的化学指纹中共有的二进制位的数量。

### 子结构

子结构主要用来计算某化学结构与其子结构的相似度。值越小则相似度越大。Milvus 目前只返回距离为 0 的结果。

子结构的公式可表示为：

![substructure](../../../assets/substructure.png)

其中

- 分子式 B 是分子式 A 的子结构。
- N<sub>A</sub> 表示分子式 A 的化学指纹中二进制位的数量。
- N<sub>B</sub> 表示分子式 B 的化学指纹中二进制位的数量。
- N<sub>AB</sub> 表示分子式 A 和 B 的化学指纹中共有的二进制位的数量。


## 常见问题

<details>
<summary><font color="#4fc4f9">为什么向量距离计算方式是内积时，搜索出来的 top1 不是目标向量本身？</font></summary>
{{fragments/faq_top1_not_target.md}}
</details>
<details>
<summary><font color="#4fc4f9">什么是归一化？Milvus 中为什么有时候需要归一化？</font></summary>
{{fragments/faq_normalize_embeddings.md}}
</details>
<details>
<summary><font color="#4fc4f9">为什么欧氏距离和内积在计算向量相似度时的结果不一致？</font></summary>
{{fragments/faq_euclidean_ip_different_results.md}}
</details>
