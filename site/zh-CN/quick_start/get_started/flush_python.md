---
id: flush_python.md
---

# 数据落盘

在进行有关数据更改的操作时，你可以将集合中的数据从内存中进行 flush 操作使数据落盘。Milvus 也会执行自动落盘。自动落盘会在固定的时间周期（1 秒）对所有现存集合的数据进行落盘操作。

```python
>>> milvus.flush(collection_name_array=['test01'])
```

<div class="alert note">
在调用 <code>delete</code> 接口后，用户可以选择再调用 <code>flush</code>，保证新增的数据可见，被删除的数据不会再被搜到。
</div>



## 常见问题

<details>
<summary><font color="#4fc4f9">为什么数据插入后不能马上被搜索到？</font></summary>
{{fragments/faq_inserted_data_unsearchable.md}}
</details>
