---
id: create_drop_collection_python.md
---

# Create and Drop a Collection

This article provides Python sample codes for creating or dropping collections.

<div class="alert note">
See <a href="https://github.com/milvus-io/pymilvus/tree/master/examples">Example Program</a> for more detailed usage.
</div>

## Create a Collection

1. Prepare the parameters needed to create the collection:

   ```python
   # Prepare collection parameters.
   >>> param = {'collection_name':'test01', 'dimension':256, 'index_file_size':1024, 'metric_type':MetricType.L2}
   ```

2. Create a collection named `test01`, with a dimension of 256 and an index file size of 1024 MB. It uses Euclidean distance (L2) as the distance measurement method.

   ```python
   # Create a collection.
   >>> milvus.create_collection(param)
   ```


## Drop a Collection

```python
# Drop a collection.
>>> milvus.drop_collection(collection_name='test01')
```

## FAQ

<details>
<summary><font color="#4fc4f9">How can I get the best performance from Milvus through setting <code>index_file_size</code>?</font></summary>
{{fragments/faq_index_file_size_best_practice.md}}
</details>
<details>
<summary><font color="#4fc4f9">Can I update <code>index_file_size</code> and <code>metric_type</code> after creating a collection?</font></summary>
{{fragments/faq_update_param_after_collection.md}}
</details>
<details>
<summary><font color="#4fc4f9">Is there a limit on the total number of collections and partitions?</font></summary>
{{fragments/faq_collection_partition_numbers.md}}
</details>
<details>
<summary><font color="#4fc4f9">What is the maximum dimension of a vector in Milvus?</font></summary>
{{fragments/faq_max_vector_dimension.md}}
</details>