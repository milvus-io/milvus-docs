---
id: create_drop_collection_python.md
---

# 创建、删除集合

本页提供创建或删除集合的 Python 示例代码。

<div class="alert note">
参考 <a href="https://github.com/milvus-io/pymilvus/tree/master/examples">示例程序</a> 获取更详细的使用方式。
</div>

## 创建集合

1. 准备创建集合所需参数：

   ```python
   # Prepare collection parameters.
   >>> param = {'collection_name':'test01', 'dimension':256, 'index_file_size':1024, 'metric_type':MetricType.L2}
   ```

2. 创建集合名为 `test01`，维度为 256，自动创建索引的数据文件大小为 1024 MB，距离度量方式为欧氏距离（L2）的集合：

   ```python
   # Create a collection.
   >>> milvus.create_collection(param)
   ```


## 删除集合

```python
# Drop a collection.
>>> milvus.drop_collection(collection_name='test01')
```

## 常见问题

<details>
<summary><font color="#3ab7f8">创建集合时 <code>index_file_size</code> 如何设置能达到性能最优？</font></summary>
{{fragments/faq_index_file_size_best_practice.md}}
</details>
<details>
<summary><font color="#3ab7f8">建立集合后，<code>index_file_size</code> 和 <code>metric_type</code> 还支持修改吗？</font></summary>
{{fragments/faq_update_param_after_collection.md}}
</details>
<details>
<summary><font color="#3ab7f8">Milvus 对集合和分区的总数有限制吗？</font></summary>
{{fragments/faq_collection_partition_numbers.md}}
</details>
