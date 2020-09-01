<p>Yes. But the parallelism processing mechanism varies with Milvus versions.
</p>
<p>
Suppose a collection has multiple segments, then when a query request comes in:
<ul>
<li>CPU-only Milvus processes the segment reading tasks and the segment searching tasks in pipeline.</li>
<li>On top of the abovementioned pipeline mechanism, GPU-enabled Milvus distributes the segments among the available GPUs.</li>
</ul>
</p>
<p>
See <a href="https://medium.com/unstructured-data-service/how-does-milvus-schedule-query-tasks-2ca38d7bc2f2">How Does Milvus Schedule Query Tasks</a> for more information.
</p>
