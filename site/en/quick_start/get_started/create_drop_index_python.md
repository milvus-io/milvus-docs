---
id: create_drop_index_python.md
---

# Create and Drop an Index

This article provides Python sample codes for creating or dropping indexes.

## Create an index

Currently, a collection only supports one index type. When you change the index type of a collection, Milvus automatically deletes the old index file. Before creating other indexes, a collection uses FLAT as the default index type.

<div class="alert note">
<code>create_index()</code> specifies the index type of a collection and synchronously creates indexes for the previously inserted data. When the size of the subsequently inserted data reaches the <code>index_file_size</code>, Milvus automatically creates indexes in the background. For streaming data, it is recommended to create indexes before inserting the vector so that the system can automatically build indexes for the next data. For static data, it is recommended to import all the data at first and then create indexes. See <a href="https://github.com/milvus-io/pymilvus/tree/master/examples/indexes">Index Sample Program</a> for details about using index.
</div>

1. Prepare the parameters needed to create indexes (take IVF_FLAT as an example). The index parameters are stored in a JSON string, which is represented by a dictionary in the Python SDK.

   ```python
   # Prepare index param.
   >>> ivf_param = {'nlist': 16384}
   ```

   <div class="alert note">
   Different index types requires different indexing parameters. They <b>must</b> all have a value.
   </div>

2. Create index for the collection:

   ```python
   # Create an index.
   >>> milvus.create_index('test01', IndexType.IVF_FLAT, ivf_param)
   ```

## Drop an Index

After deleting the index, the collection uses the default index type FLAT again.

```python
>>> milvus.drop_index('test01')
```

## FAQ

<details>
<summary><font color="#4fc4f9">How to set the value of <code>nlist</code> when I build indexes?</font></summary>
{{fragments/faq_set_nlist.md}}
</details>
<details>
<summary><font color="#4fc4f9">Can Milvus create different types of index for different partitions in the same collection?</font></summary>
{{fragments/faq_collection_different_index.md}}
</details>
<details>
<summary><font color="#4fc4f9">Does Milvus create new indexes after vectors are inserted?</font></summary>
{{fragments/faq_create_index_after_insertion.md}}
</details>

