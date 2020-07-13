---
id: overview.md
---

# Milvus 简介





## 术语

- 实体（Entity）: 代表一个实际对象，由字段组成。

- 字段（Field）：用于表示对象的某个属性。字段可以是结构化数据，也可以是向量。

- 实体标识（Entity ID）: 是用于唯一指代一个实体的 64 位非负整数。创建实体时，该标识可以由用户指定，也可以由 Milvus 自动生成。

<div class="alert note">
目前，Milvus 不支持标识去重，因此你需要保证插入实体标识的唯一性。
</div>

- 集合（Collection）: 包含一组同类实体，可以理解为关系型数据库系统中的表。

- 段（Segment）: 为了能处理大规模的数据，Milvus 会将数据分段。一个集合可以包含多个段。

- 分区（Partition）: 用于将集合中的数据划分为几个独立的部分。

- 索引（Index）：一种加速数据检索的数据结构。

- 映射（Mapping）: 一个集合中数据的组织形式，可以理解为关系型数据库系统中的 Schema。

- 向量（Vector）：一种由 N 维数组成的数据类型。是事物特征的抽象，可用于表征某个事物。

<div class="alert note">
注意：目前，一个实体最多只能包含一个向量。
</div>





## 接下来你可以

- 了解 [特征向量](vector.md), [向量数据库](vector_db.md) 的发展现状和 [向量检索算法](index_method.md)
- 几分钟轻易搞定 [Milvus 安装](install_milvus.md)
