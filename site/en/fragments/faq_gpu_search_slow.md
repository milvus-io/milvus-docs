Generally speaking, CPU-only query works for situations where <code>nq</code> (number of vectors per query) is small, whilst GPU-enabled query works best with a large <code>nq</code>, say 500.

Milvus needs to load data from the memory to the graphics memory for a GPU-enabled query. Only when the load time is negligible compared to the time to query, is GPU-enabled query faster.