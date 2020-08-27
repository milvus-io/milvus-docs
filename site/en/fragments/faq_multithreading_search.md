If your batch query is on a small scale (`nq` < 64), Milvus combines the query requests, in which case multi-threading helps.

Otherwise, the resources are already exhausted, hence multi-threading does not help much.