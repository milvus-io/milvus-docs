---
id: metric-floating.md
label: Floating point vectors
order: 0
group: vectors
---

{{fragments/metrics.md}}

{{tab}} 

<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky" style="width: 204px;">Distance Metrics</th>
    <th class="tg-0pky">Index Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky">Euclidean distance (L2)</td>
    <td class="tg-0pky" rowspan="2"><ul><li>FLAT</li><li>IVF_FLAT</li><li>IVF_SQ8</li><li>IVF_SQ8H</li><li>IVF_PQ</li><li>RNSG</li><li>HNSW</li></ul></td>
  </tr>
  <tr>
    <td class="tg-0pky">Inner product (IP)</td>
  </tr>
</tbody>
</table>

### Euclidean distance (L2)

Essentially, Euclidean distance measures the length of a segment that connects 2 points.

The formula for Euclidean distance is as follows:

![euclidean](../../../assets/euclidean_metric.png)

where **a** = (a1, a2,..., an) and **b** = (b1, b2,..., bn) are two points in n-dimensional Euclidean space

It's the most commonly used distance metric, and is very useful when the data is continuous.

### Inner product (IP)

The IP distance between two embeddings are defined as follows: 

![ip](../../../assets/IP_formula.png)

where A and B are embeddings, `||A||` and `||B||` are the norms of A and B.

IP is more useful if you are more interested in measuring the orientation but not the magnitude of the vectors.

<div class="alert note">
 If you use IP to calculate embeddings similarities, you must normalize your embeddings. After normalization, inner product equals cosine similarity.
</div>


Suppose X' is normalized from embedding X: 

![normalize](../../../assets/normalize_formula.png)

The correlation between the two embeddings is as follows: 

![normalization](../../../assets/normalization_formula.png)


## FAQ

<details>
<summary><font color="#4fc4f9">Why is the top1 result of a vector search not the search vector itself, if the metric type is inner product?</font></summary>
{{fragments/faq_top1_not_target.md}}
</details>
<details>
<summary><font color="#4fc4f9">What is normalization? Why is normalization needed?</font></summary>
{{fragments/faq_normalize_embeddings.md}}
</details>
<details>
<summary><font color="#4fc4f9">Why do I get different results using Euclidean distance (L2) and inner product (IP) as the distance metric?</font></summary>
{{fragments/faq_euclidean_ip_different_results.md}}
</details>
