---
id: create_drop_index_python.md
---

# 创建、删除索引

本页提供创建或删除索引的 Python 示例代码。

## 创建索引

目前，一个集合的每个字段只支持一种索引类型，切换索引类型会自动删除旧的索引文件。在创建其它索引前，FLAT 作为集合的默认索引类型。

<div class="alert note">
</div>

1. 准备创建索引所需参数（以向量字段创建索引 IVF_FLAT 为例）。索引参数是一个 JSON 字符串，在 Python SDK 中以字典来表示。

   ```python
   # Prepare index param.
   >>> ivf_param = {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 4096}}
   ```

   <div class="alert note">
   对于不同的索引类型，创建索引所需参数也有区别。所有的索引参数都<b>必须赋值</b>。详细信息请参考 <a href="index.md">Milvus 索引类型</a>。
   </div>


2. 为指定集合创建索引：

   ```python
   # Create an index.
   >>> client.create_index('test01', "Vec", ivf_param)
   ```

## 删除索引

删除索引后，向量字段再次使用默认索引类型 FLAT。

```python
>>> client.drop_index('test01')
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

