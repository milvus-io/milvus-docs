---
id: create_drop_index_python.md
---

# 创建、删除索引

本页提供创建或删除索引的 Python 示例代码。

## 创建索引

目前，一个集合只支持一种索引类型，切换索引类型会自动删除旧的索引文件。在创建其它索引前，FLAT 作为集合的默认索引类型。

<div class="alert note">
<code>create_index()</code> 会指定该集合的索引类型，并同步为之前插入的数据建立索引，后续插入的数据在大小达到 <code>index_file_size</code> 时，索引会在后台自动建立。在实际生产环境中，如果是流式数据，建议在插入向量之前先创建索引，以便后续系统自动建立；如果是静态数据，建议导入所有数据后再一次性创建索引。更多索引用法请参考 <a href="https://github.com/milvus-io/pymilvus/tree/master/examples/indexes">索引示例程序</a>。
</div>

1. 准备创建索引所需参数（以 IVF_FLAT 为例）。索引参数是一个 JSON 字符串，在 Python SDK 中以字典来表示。

   ```python
   # Prepare index param.
   >>> ivf_param = {'nlist': 16384}
   ```

   <div class="alert note">
   对于不同的索引类型，创建索引所需参数也有区别。所有的索引参数都<b>必须赋值</b>。详细信息请参考 <a href="index.md">Milvus 索引类型</a>。
   </div>


2. 为指定集合创建索引：

   ```python
   # Create an index.
   >>> milvus.create_index('test01', IndexType.IVF_FLAT, ivf_param)
   ```

## 删除索引

删除索引后，集合再次使用默认索引类型 FLAT。

```python
>>> milvus.drop_index('test01')
```

## 常见问题

<details>
<summary><font color="#4fc4f9">建索引参数 <code>nlist</code> 的大小该如何选择？</font></summary>
{{fragments/faq_set_nlist.md}}
</details>
<details>
<summary><font color="#4fc4f9">Milvus 可以在同一个集合中的不同分区上建立不同索引吗？</font></summary>
{{fragments/faq_collection_different_index.md}}
</details>
<details>
<summary><font color="#4fc4f9">Milvus 中支持新增向量后再建索引吗？</font></summary>
{{fragments/faq_create_index_after_insertion.md}}
</details>

