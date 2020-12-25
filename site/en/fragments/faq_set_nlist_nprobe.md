In general terms, the recommended value of `nlist` is `4 * sqrt(n)`, where n is the total number of vectors in the dataset. 

Determining `nprobe` is a trade-off between search performance and accuracy, and based on your dataset and scenario. It is recommended to run several rounds of tests to determine the value of `nprobe`.

The following charts are from a test running on the sift50m dataset and IVF\_SQ8 index. The test compares search performance and recall rate between different `nlist`/`nprobe` pairs.

<div class="alert note">

We only show the results of GPU-enabled Milvus here, because the two distributions of Milvus show similar results.

</div>

![Accuracy](../../../assets/accuracy_nlist_nprobe.png)

Key takeaways: This test shows that the recall rate increases with the `nlist`/`nprobe` pair.

![Performance](../../../assets/performance_nlist_nprobe.png)

Key takeaways: When `nlist` is 4096 and `nprobe` 128, Milvus shows the best search performance.
