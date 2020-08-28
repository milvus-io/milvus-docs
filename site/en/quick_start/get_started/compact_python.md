---
id: compact_python.md
---

# Compact Segments

Milvus automatically merges the inserted vector data to segments. A collection can contain multiple segments. After deleting some vector data in a segment, the system cannot automatically release the space occupied by the deleted vector data. So, you need to compact the segments in the collection to free up extra space.

```python
>>> milvus.compact(collection_name='test01', timeout='1')
```

## FAQ

<details>
<summary><font color="#3f9cd1">Does Milvus' Python SDK have a connection pool?</font></summary>
{{fragments/faq_pymilvus_connection_pool.md}}
</details>
<details>
<summary><font color="#3f9cd1">How to fix the error when I install pymilvus on Windows?</font></summary>
{{fragments/faq_pymilvus_install_error.md}}
</details>
