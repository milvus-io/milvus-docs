Milvus comes in two distributions: CPU-only Milvus and GPU-enabled Milvus.

<ul>
<li>CPU-only Milvus only supports searching after index building completes, and hence is applicable to static datasets.</li> 
<li>GPU-enabled Milvus supports GPU acceleration for searching and index building: It supports searching and index building at the same time to improve query efficiency, and hence is applicable to dynamic datasets.</li>
</ul>

If your GPU supports CUDA, then you can install GPU-enabled Milvus to achieve much higher search performance in large-scale datasets.