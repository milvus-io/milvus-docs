---
id: search_entity_python.md
---

# Conduct a Vector Search

Milvus supports searching vectors in a collection or partition.

## Search for vectors in a collection

1. Create search parameters. The search parameters are stored in a JSON string, which is represented by a dictionary in the Python SDK.

   ```python
   >>> search_param = {'nprobe': 16}
   ```

   <div class="alert note">
   Different index types requires different search parameters. You must <b>assign values</b> to all search parameters. See <a href="index.md">Vector Indexes</a> for more information. 
   </div>



2. Create random vectors as `query_records` to search:

   ```python
   # Create 5 vectors of 256 dimensions.
   >>> q_records = [[random.random() for _ in range(256)] for _ in range(5)]
   >>> milvus.search(collection_name='test01', query_records=q_records, top_k=2, params=search_param)
   ```
   <div class="alert note">
   <ul><li><code>top_k</code> means searching the k vectors most similar to the target vector. It is defined during the search.</li><li>The range of <code>top_k</code> is [1, 16384].</li></ul>
   </div>

## Search vectors in a partition

```python
# Create 5 vectors of 256 dimensions.
>>> q_records = [[random.random() for _ in range(256)] for _ in range(5)]
>>> milvus.search(collection_name='test01', query_records=q_records, top_k=1, partition_tags=['tag01'], params=search_param)
```

<div class="alert note">
If you do not specify <code>partition_tags</code>, Milvus searches similar vectors in the entire collection.
</div>


## FAQ

<details>
<summary><font color="#4fc4f9">Why is my recall rate unsatisfying?</font></summary>
{{fragments/faq_poor_recall_rate.md}}
</details>
<details>
<summary><font color="#4fc4f9">Does Milvus support inserting while searching?</font></summary>
{{fragments/faq_search_during_insert.md}}
</details>
<details>
<summary><font color="#4fc4f9">Does the size of a collection affect vector searches in one of its partitions, especially when it holds up to 100 million vectors?</font></summary>
{{fragments/faq_collection_affect_partition_search.md}}
</details>
<details>
<summary><font color="#4fc4f9">Does Milvus load the whole collection to the memory if I search only certain partitions in that collection?</font></summary>
{{fragments/faq_load_when_search_partition.md}}
</details>
<details>
<summary><font color="#4fc4f9">Are queries in segments processed in parallel?</font></summary>
{{fragments/faq_search_segment_parallel.md}}
</details>
<details>
<summary><font color="#4fc4f9">Will a batch query benefit from multi-threading?</font></summary>
{{fragments/faq_multithreading_search.md}}
</details>
<details>
<summary><font color="#4fc4f9">Why the search is very slow?</font></summary>
{{fragments/faq_search_slow.md}}
</details>
<details>
<summary><font color="#4fc4f9">Why do I see a surge in memory usage when conducting a vector search immediately after an index is created?</font></summary>
{{fragments/faq_search_increase_memory_usage.md}}
</details>
<details>
<summary><font color="#4fc4f9">Why does the first search take a long time after Milvus restarts?</font></summary>
{{fragments/faq_search_time_after_restart.md}}
</details>
