<p>It is very likely that Milvus is using CPU for query. If you want to use GPU for query, you need to set the value of <code>gpu_search_threshold</code> in <strong>server_config.yaml</strong> to be less than <code>nq</code> (number of vectors per query).
</p>
<p>
You can use <code>gpu_search_threshold</code> to set the threshold: when <code>nq</code> is less than this value, Milvus uses CPU for queries; otherwise, Milvus uses GPU instead.
</p>
<p>
We do not recommend enabling GPU when the query number is small.
</p>