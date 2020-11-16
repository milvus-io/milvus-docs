---
id: search_entity.md
---

# Conduct a Vector Search

Milvus supports searching vectors in a collection or partition.

## Search for vectors in a collection

1. Create search parameters DSL.

      <div class="filter">
   <a href="#Python">Python</a> <a href="#Java">Java</a>
   </div>

   <div class="filter-Python" markdown="block">

   ```python
   # This DSL searches for topk `entities` that are
   # closest to vectors[:1] searched by `IVF_FLAT` index with `nprobe = 10` and `metric_type = L2`,
   # AND field "A" in [1, 2, 5],
   # AND field "B" greater than 1 less than 100
   >>> dsl = {
   ...     "bool": {
   ...         "must":[
   ...             {
   ...                 "term": {"A": [1, 2, 5]}
   ...             },
   ...             {
   ...                 "range": {"B": {"GT": 1, "LT": 100}}
   ...             },
   ...             {
   ...                 "vector": {
   ...                    "Vec": {"topk": 10, "query": vectors[:1], "metric_type": "L2", "params": {"nprobe": 10}}
   ...                 }
   ...             }
   ...         ]
   ...     }
   ... }
   ```
   </div>

   <div class="filter-Java" markdown="block">

   ```java
   // Basic hybrid search:
   // Let's say we have a film with its `embedding` and we want to find `top1` film that is
   // most similar to it by L2 metric_type (Euclidean Distance).
   // In addition to vector similarities, we also want to filter films such that:
   // - `term` is 1, 2, or 5,
   // - `duration` larger than 250 minutes.
   List<List<Float>> queryEmbedding = /* your query vectors */;
    final long topK = 10;
    String dsl = String.format(
        "{\"bool\": {"
            + "\"must\": [{"
            + "    \"range\": {"
            + "        \"A\": {\"GT\": 250}" // "GT" for greater than
            + "    }},{"
            + "    \"term\": {"
            + "        \"B\": [1, 5, 10]" // "term" is a list
            + "    }},{"
            + "    \"vector\": {"
            + "        \"embedding\": {"
            + "            \"topk\": %d, \"metric_type\": \"L2\", \"type\": \"float\", \"query\": %s"
            + "    }}}]}}", topK, queryEmbedding.toString());
   ```
   </div>

   <div class="alert note">
   <ul>
   <li><code>topk</code> refers to the k vectors closest to the target vector in the vector space.</li>
   <li>The range of <code>topk</code> is [1, 16384].</li>
   <li>Different index requires different search parameters. To conduct an embedding search, you <b>must</b> assign values to all search parameters. See <a href="index.md">Vector Indexes</a> for more information. </li>  
   </ul>
   </div>



2. Conduct a similarity search:

     <div class="filter">
   <a href="#Python">Python</a> <a href="#Java">Java</a>
   </div>

   <div class="filter-Python" markdown="block">

   ```python
   >>> client.search('test01', dsl)
   ```
   </div>

   <div class="filter-Java" markdown="block">

   ```java
   SearchParam searchParam = SearchParam
    .create(collectionName)
    .setDsl(dsl);

   SearchResult searchResult = client.search(searchParam);
   ```
   </div>

You can also set Milvus to return a specified field. Here, we retrieve values in the `B` field:

<div class="filter">
   <a href="#Python">Python</a> <a href="#Java">Java</a>
   </div>

   <div class="filter-Python" markdown="block">

   ```python
   >>> client.search('test01', dsl, fields=["B"])
   ```
   </div>
   
   <div class="filter-Java" markdown="block">

   ```java
   SearchParam searchParam = SearchParam
        .create(collectionName)
        .setDsl(dsl)
        .setParamsInJson("{\"fields\": [\"B\"]}");
   SearchResult searchResult = client.search(searchParam);
   ```
   </div>

## Search vectors in a partition

<div class="filter">
<a href="#Python">Python</a> <a href="#Java">Java</a>
</div>

<div class="filter-Python" markdown="block">

```python
>>> client.search('test01', dsl, partition_tags=['tag01'])
```
</div>

<div class="filter-Java" markdown="block">

```java
setPartitionTags​(java.util.List<java.lang.String> partitionTags);
```
</div>

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
