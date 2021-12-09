---
id: insight_collection.md
related_key: insight
summary: Milvus Insight, an intuitive GUI for Milvus service management.
---

# 使用 Insight 管理 Collections

这片文章将会描述如何使用 Insight 管理 Collections

## 创建 Collection

1. 点击左侧导航的 **Collection** 标签，然后点击 **Create Collection**。如下图所示，将会出现弹窗 **Create Collection**。

![Create Collection dialog box](../../../../assets/create_collection_dialog_box1.png)

2. 填写相应表单，这个例子将创建了名为 test 的 collection，同时有一个主键，一个向量字段，一个标量字段。你也可以继续添加需要的标量字段。

![Create Collection dialog box](../../../../assets/create_collection_dialog_box2.png)

3. 点击 **Create** 就可以创建我们第一个 collection！

![Create Collection dialog box](../../../../assets/create_collection_dialog_box3.png)

## 删除 Collection

1. 在表格里，选中需要删除的 collection。
2. 点击 **Trash** 图标，如下图所示，将会出现弹窗 **Delete Collection**
3. 输入 `delete` 用来确认删除操作
4. 点击 **Delete** 将会删除选中的所有 collection。

<div class="alert caution">
删除操作是不可回滚的。
</div>

![Delete Collection dialog box](../../../../assets/delete_collection.png)

## 加载 collection

1. 鼠标悬浮在需要加载的 collection 行上，**Load** 图标将会出现在该行末尾。

![Load Collection](../../../../assets/load_collection1.png)

2. 点击 **Load** 图标，将会出现 **Load Collection** 窗口
3. 点击窗口中的 **Load** 按钮

![Load Collection](../../../../assets/load_collection2.png)

4. 加载 collection 数据到缓存中可能需要一些时间。当加载完成后，Status 列将会变成 **Loaded For Search**。

![Load Collection](../../../../assets/load_collection3.png)

## 释放 Collection

1. 鼠标悬浮在需要加载的 collection 行上，**Release** 图标将会出现在该行末尾。

![Release Collection](../../../../assets/release_collection1.png)

2. 点击 **Release** 图标，将会出现 **Release Collection** 窗口
3. 点击窗口中的 **Release** 按钮
4. 如果释放成功，Status 列将会变成 **Unloaded**。

![Release Collection](../../../../assets/release_collection2.png)

## 查看 collection 的 schema

1. 点击数据行的 collection name，跳转到 collection 详情页面。
2. 在详情页点击 **Schema**，就可以看到 schema 的相关信息。

schema 的属性包含：

- Field Name
- Field Type
- Dimension (向量字段才有数据)
- Index Type (向量字段才有数据)
- Index Parameters (向量字段才有数据)
- Collection description

![Collection Schema](../../../../assets/collection_schema.png)
