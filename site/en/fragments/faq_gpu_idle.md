It is very likely that Milvus is using CPU for query. If you want to use GPU for query, you need to set the value of `gpu_search_threshold` in **server_config.yaml** to be greater than `nq` (number of vectors per query).

You can use `gpu_search_threshold` to set the threshold: when `nq` is less than this value, Milvus uses CPU for queries; otherwise, Milvus uses GPU instead.

We do not recommend enabling GPU when the query number is small.
