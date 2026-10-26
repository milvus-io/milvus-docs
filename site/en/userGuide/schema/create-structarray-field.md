---
id: create-structarray-field.md
title: "Create a StructArray Field"
summary: "Create a StructArray field when one entity needs to contain an ordered list of structured elements. A StructArray field is an Array field whose element type is Struct. Each Struct element follows the same schema and can contain scalar subfields, vector subfields, and, starting in Milvus 3.1.0, scalar array subfields."
---
# Create a StructArray Field

Create a StructArray field when one entity needs to contain an ordered list of structured elements. A StructArray field is an Array field whose element type is Struct. Each Struct element follows the same schema and can contain scalar subfields, vector subfields, and, starting in Milvus 3.1.0, scalar array subfields.

This page shows how to define a Struct schema, add it as a StructArray field, choose subfields for later search and filtering, and understand the schema rules that apply before you insert or index data.

## Before you begin

This page uses a collection named `tech_articles`. Each entity represents one technical article, and the `chunks` field stores chunk-level data as Struct elements.

| Field | Type | Purpose |
| --- | --- | --- |
| `doc_id` | `INT64` | Primary key for the article. |
| `title` | `VARCHAR` | Article title. |
| `category` | `VARCHAR` | Article-level category. |
| `title_vector` | `FLOAT_VECTOR` | Article-level vector field, used later in hybrid search examples. |
| `chunks` | `ARRAY` | StructArray field that stores chunk-level text, metadata, and embeddings. |

The `chunks` StructArray field contains the following subfields.

| Subfield | Type | Purpose |
| --- | --- | --- |
| `text` | `VARCHAR` | Chunk text. |
| `section` | `VARCHAR` | Section name, such as `index`, `search`, or `filter`. |
| `page` | `INT64` | Page number or logical position of the chunk. |
| `quality_score` | `FLOAT` | Chunk-level score used in scalar filtering and range examples. |
| `has_code` | `BOOL` | Whether the chunk contains code. |
| `emb_list_vector` | `FLOAT_VECTOR` | Vector subfield for EmbeddingList search with `MAX_SIM*` metrics. |
| `emb` | `FLOAT_VECTOR` | Vector subfield for element-level search with regular vector metrics. |

<div class="alert note">

A vector field or vector subfield accepts only one index. If you need both EmbeddingList search and element-level search, define two separate vector subfields. In this example, `chunks[emb_list_vector]` is for EmbeddingList search, and `chunks[emb]` is for element-level search.

</div>

## Supported subfield data types

A StructArray field stores one array value for each Struct subfield. When you define a Struct schema, choose subfield types from the supported scalar, scalar array (Milvus 3.1.0 and later), and vector families.

| Struct subfield physical type | Support | Notes |
| --- | --- | --- |
| `Array` | Supported | Define the subfield as `DataType.BOOL`. |
| `Array` | Supported | Define the subfield as `DataType.INT8`, `DataType.INT16`, `DataType.INT32`, or `DataType.INT64`. |
| `Array` | Supported | Define the subfield as `DataType.FLOAT` or `DataType.DOUBLE`. |
| `Array` | Supported | Define the subfield as `DataType.VARCHAR` and set `max_length`. |
| `ArrayOfVector` | Supported | Define the subfield as `DataType.FLOAT_VECTOR` and set `dim`. |
| `ArrayOfVector` | Supported | Define the subfield as `DataType.FLOAT16_VECTOR` and set `dim`. |
| `ArrayOfVector` | Supported | Define the subfield as `DataType.BFLOAT16_VECTOR` and set `dim`. |
| `ArrayOfVector` | Supported | Define the subfield as `DataType.INT8_VECTOR` and set `dim`. |
| `ArrayOfVector` | Supported | Define the subfield as `DataType.BINARY_VECTOR` and set `dim`. |
| `ArrayOfVector` | Not supported | Sparse vector subfields are not supported in StructArray fields. |
| `Array` | Not supported | Use `VARCHAR`, not `String`. |
| `Array` | Not supported | JSON subfields are not supported in StructArray fields. |
| `Array` | Not supported | Geometry subfields and GIS functions are not supported in StructArray fields. |
| `Array` | Not supported | Text subfields are not supported in StructArray fields. |
| `Array` | Not supported | Timestamptz subfields and time-specific expressions are not supported in StructArray fields. |
| `Array` of `Array` | Supported in Milvus 3.1.0 and later | Define the subfield as `DataType.ARRAY` with a scalar `element_type` and a `max_capacity` for the inner array. Each Struct element then holds one inner array. |
| `Array` of `Array` of `Array`, `Array` of vectors, `Struct`, or `ArrayOfStruct` | Not supported | Array nesting inside a Struct is limited to one level, the inner array cannot hold vectors, and a Struct cannot contain nested Struct or Array-of-Struct subfields. |

For version-specific support, nullable behavior, and other limits, see [StructArray Limits](structarray-limits.md).

## Create a collection with a StructArray field

To create a StructArray field, first define the Struct schema used by each element. Then add an Array field and set its element type to Struct.

1. Create the collection schema.

2. Add collection-level fields, such as the primary key and article-level fields.

3. Create a Struct schema for elements stored inside the StructArray field.

4. Add scalar and vector subfields to the Struct schema.

5. Add an Array field with `element_type=DataType.STRUCT`.

6. Set `struct_schema` to the Struct schema.

7. Set `max_capacity` to limit how many Struct elements each entity can store in the field.

```python
from pymilvus import MilvusClient, DataType

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus",
)

schema = client.create_schema(
    auto_id=False,
    enable_dynamic_field=False,
)

# Collection-level fields.
schema.add_field(
    field_name="doc_id",
    datatype=DataType.INT64,
    is_primary=True,
)
schema.add_field(
    field_name="title",
    datatype=DataType.VARCHAR,
    max_length=512,
)
schema.add_field(
    field_name="category",
    datatype=DataType.VARCHAR,
    max_length=128,
)
schema.add_field(
    field_name="title_vector",
    datatype=DataType.FLOAT_VECTOR,
    dim=4,
)

# Struct schema used by each element in the StructArray field.
chunk_schema = client.create_struct_field_schema()
chunk_schema.add_field(
    field_name="text",
    datatype=DataType.VARCHAR,
    max_length=65535,
)
chunk_schema.add_field(
    field_name="section",
    datatype=DataType.VARCHAR,
    max_length=128,
)
chunk_schema.add_field(
    field_name="page",
    datatype=DataType.INT64,
)
chunk_schema.add_field(
    field_name="quality_score",
    datatype=DataType.FLOAT,
)
chunk_schema.add_field(
    field_name="has_code",
    datatype=DataType.BOOL,
)

# Vector subfield for EmbeddingList search.
chunk_schema.add_field(
    field_name="emb_list_vector",
    datatype=DataType.FLOAT_VECTOR,
    dim=4,
)

# Vector subfield for element-level search.
chunk_schema.add_field(
    field_name="emb",
    datatype=DataType.FLOAT_VECTOR,
    dim=4,
)

# Add the StructArray field.
schema.add_field(
    field_name="chunks",
    datatype=DataType.ARRAY,
    element_type=DataType.STRUCT,
    struct_schema=chunk_schema,
    max_capacity=1000,
)

client.create_collection(
    collection_name="tech_articles",
    schema=schema,
)
```

## Add a scalar array subfield | Milvus 3.1.0

Starting in Milvus 3.1.0, a Struct subfield can be a scalar `ARRAY`. Each Struct element then holds one inner array, such as a list of tags for each chunk. Define the subfield with `DataType.ARRAY`, a scalar `element_type`, and a `max_capacity` for the inner array.

```python
chunk_schema.add_field(
    field_name="tags",
    datatype=DataType.ARRAY,
    element_type=DataType.VARCHAR,
    max_capacity=16,
    max_length=64,
)
```

Array subfields follow these rules:

- The inner array holds scalar values only. It cannot hold vectors, Struct elements, or another array.

- The `max_capacity` of the subfield limits the inner array. The `max_capacity` of the StructArray field still limits the number of Struct elements.

- Scalar indexes are not supported on array subfields.

- In filters, use `array_contains`, `array_contains_any`, `array_contains_all`, and `array_length` on `$[tags]` inside `element_filter` or `MATCH_*`, or on a positional path such as `chunks[0][tags]`. For details, see [StructArray Operators](struct-array-operators.md).

## Allow null values in Struct elements | Milvus 3.1.0

Starting in Milvus 3.1.0, set `element_nullable=True` on a scalar, vector, or array subfield to allow a null value for that subfield in individual Struct elements. For example, a chunk can have no detected language while its other subfields hold values.

```python
chunk_schema.add_field(
    field_name="lang",
    datatype=DataType.VARCHAR,
    max_length=16,
    element_nullable=True,
)
```

Element-level null follows these rules:

- `element_nullable` applies to a subfield value inside a Struct element. Row-level `nullable` still applies to the whole StructArray field and is set on the parent field only; a subfield cannot set `nullable` on its own.

- A Struct element itself cannot be null. Set the subfield values of the element to null instead.

- When you insert data, you can omit an element-nullable subfield from a Struct element or set it to `None`. Both store a null value. A subfield without `element_nullable` must be present in every Struct element.

- On an array subfield, `element_nullable=True` allows a null inner array for a Struct element. An empty inner array is not null.

- A vector subfield with `element_nullable=True` supports element-level search only. `MAX_SIM*` metrics and EmbeddingList search are rejected on it, and null vectors do not participate in search.

- Scalar indexes are not supported on element-nullable subfields.

- In filters, a null subfield value makes the element predicate unknown rather than false. Use `$[lang] is null` or `$[lang] is not null` inside `element_filter` or `MATCH_*` to test it. For details, see [StructArray Operators](struct-array-operators.md).

## Understand StructArray field paths

After you create a StructArray field, refer to its subfields with the `structArray[subfield]` path syntax. Use this syntax when you create indexes, search vector subfields, output subfields, or build scalar filters.

| Path | Meaning | Common usage |
| --- | --- | --- |
| `chunks[text]` | The `text` subfield inside each Struct element. | Output field or scalar filtering. |
| `chunks[section]` | The section label for each chunk. | Scalar filtering. |
| `chunks[quality_score]` | The chunk-level quality score. | Scalar filtering or scalar index. |
| `chunks[emb_list_vector]` | The vector subfield used as an embedding list. | EmbeddingList search with `MAX_SIM*`. |
| `chunks[emb]` | The vector subfield used by each Struct element independently. | Element-level vector search. |

## Make a StructArray field nullable

Milvus v3.0.x supports nullable StructArray fields. A nullable StructArray field allows an entity to store `null` for the entire StructArray field.

```python
schema.add_field(
    field_name="chunks",
    datatype=DataType.ARRAY,
    element_type=DataType.STRUCT,
    struct_schema=chunk_schema,
    max_capacity=1000,
    nullable=True,
)
```

<div class="alert note">

Warning
Nullable StructArray fields are available only in Milvus v3.0.x and later. For a nullable StructArray field, an entity can provide a valid StructArray value or set the whole field to `null`. A Struct element itself cannot be null. In Milvus v3.0.x, every Struct element must provide a value for every subfield. Starting in Milvus 3.1.0, subfields created with `element_nullable=True` can hold null values in individual Struct elements; see [Allow null values in Struct elements](#allow-null-values-in-struct-elements--milvus-310). For details, see [StructArray Limits](structarray-limits.md).

</div>

## Add a StructArray field to an existing collection

Milvus v3.0.x supports adding a StructArray field to an existing collection. The added StructArray field must be nullable, because entities that already exist in the collection do not have values for the new field.

To add a StructArray field to an existing collection, define the Struct schema first. Then call `add_collection_struct_field()` and set `nullable=True`.

```python
chunk_schema = client.create_struct_field_schema()
chunk_schema.add_field(
    field_name="text",
    datatype=DataType.VARCHAR,
    max_length=65535,
)
chunk_schema.add_field(
    field_name="section",
    datatype=DataType.VARCHAR,
    max_length=128,
)
chunk_schema.add_field(
    field_name="page",
    datatype=DataType.INT64,
)
chunk_schema.add_field(
    field_name="quality_score",
    datatype=DataType.FLOAT,
)
chunk_schema.add_field(
    field_name="has_code",
    datatype=DataType.BOOL,
)
chunk_schema.add_field(
    field_name="emb_list_vector",
    datatype=DataType.FLOAT_VECTOR,
    dim=4,
)
chunk_schema.add_field(
    field_name="emb",
    datatype=DataType.FLOAT_VECTOR,
    dim=4,
)

client.add_collection_struct_field(
    collection_name="tech_articles",
    field_name="chunks",
    struct_schema=chunk_schema,
    max_capacity=1000,
    nullable=True,
)
```

After the StructArray field is added, existing entities return `null` for the new field across all its subfields.

### Add a subfield to an existing StructArray field | Milvus 3.1.0

Starting in Milvus 3.1.0, you can add a subfield to a StructArray field that already holds data. Call `add_collection_field()` with the subfield path as the field name and set `element_nullable=True`. The new subfield inherits the row-level `nullable` setting and the `max_capacity` of the StructArray field.

```python
client.add_collection_field(
    collection_name="tech_articles",
    field_name="chunks[lang]",
    data_type=DataType.VARCHAR,
    max_length=16,
    element_nullable=True,
)
```

Adding a subfield follows these rules:

- The added subfield must have `element_nullable=True` and cannot have a default value. Existing entities return null for the new subfield in each of their Struct elements, and entities whose StructArray field is null stay null.

- The subfield can be a scalar, a vector, or a scalar array. Milvus appends it after the existing subfields.

- You cannot bind an index while adding the subfield. Create the index with a separate `create_index()` call. An added vector subfield supports element-level metrics only, and the collection must have an index on it before you load the collection with the new subfield included.

- Clients that omit the new subfield when inserting keep working, because Milvus stores null for omitted element-nullable subfields.

In earlier versions, drop the StructArray field and add it again with the updated Struct schema. Dropping the field removes its data.

```python
client.drop_collection_field(
    collection_name="tech_articles",
    field_name="chunks",
)

client.add_collection_struct_field(
    collection_name="tech_articles",
    field_name="chunks",
    struct_schema=updated_chunk_schema,
    max_capacity=1000,
    nullable=True,
)
```

### Drop a subfield from a StructArray field | Milvus 3.1.0

Starting in Milvus 3.1.0, you can drop a subfield from an existing StructArray field by its path. Milvus removes the subfield, its data, and its index.

```python
client.drop_collection_field(
    collection_name="tech_articles",
    field_name="chunks[lang]",
)
```

You cannot drop the last subfield of a StructArray field, the last vector field of the collection, or a subfield used by a Function. To remove the whole StructArray field, drop the field by its name, such as `chunks`. After a subfield is dropped, insert requests that still carry the subfield are rejected.

## Schema rules

| Rule | Explanation |
| --- | --- |
| Struct is used as an Array element type. | Create a StructArray field as an Array field with `element_type=STRUCT`. Do not create Struct as a top-level collection field. |
| All elements share one schema. | Every Struct element in the same StructArray field follows the Struct schema defined for that field. |
| `max_capacity` is required. | It limits how many Struct elements each entity can store in the StructArray field. |
| Only supported subfield types are allowed. | Use scalar, scalar array (Milvus 3.1.0 and later), and vector subfield types supported by StructArray. Do not define JSON, Geometry, Text, Timestamptz, SparseFloatVector, or nested Struct subfields. |
| Vector subfields need indexes before search. | Create indexes on paths such as `chunks[emb_list_vector]` or `chunks[emb]` before running vector search. |
| One vector subfield has one index. | If you need both EmbeddingList search and element-level search, create two separate vector subfields. |
| Subfields can change only in Milvus 3.1.0 and later. | Add an element-nullable subfield or drop a subfield by its path. In earlier versions, drop the StructArray field and add it again with the updated schema. |
| All subfields share one `max_capacity`. | The StructArray field's `max_capacity` applies to every subfield. An added subfield inherits it. |
| Functions are not supported inside Struct. | Do not define functions for fields or subfields inside a StructArray field. |
| Scalar subfields should match filter needs. | Add fields such as `section`, `quality_score`, or `has_code` only when you need to filter, group, or output them later. |

## Common mistakes

- Creating `DataType.STRUCT` as a top-level collection field instead of using it as the element type of an Array field.

- Forgetting to set `max_capacity` on the StructArray field.

- Defining unsupported subfield types, such as JSON, Geometry, Text, Timestamptz, SparseFloatVector, nested Struct, Array-of-Struct, or an array subfield that holds vectors or another array.

- Using `String` as a subfield type. Use `VARCHAR` and set `max_length`.

- Using one vector subfield for both EmbeddingList search and element-level search.

- Adding only vector subfields and forgetting scalar subfields needed for filtering, such as `section`, `quality_score`, or `has_code`.

- Treating vector subfields as `$[...]` scalar predicate inputs. Use vector subfields for vector search, and scalar subfields for scalar predicates.

- Assuming new subfields can be added to an existing StructArray field before Milvus 3.1.0, or adding a subfield without `element_nullable=True`.

- Setting `nullable=True` on a subfield. Row-level null is set on the StructArray parent; use `element_nullable=True` for null values inside Struct elements.

- Using `chunks.emb` or `chunks.emb_list_vector` instead of the required path syntax `chunks[emb]` or `chunks[emb_list_vector]`.

- Treating nullable StructArray behavior as available in every target version.

## Next steps

1. To insert nested data into the StructArray field, read [Insert Data into StructArray Fields](insert-data-into-structarray-fields.md).

2. To create vector and scalar indexes, read [Index StructArray Fields](index-structarray-fields.md).

3. To search StructArray vector subfields, read [Basic Vector Search with StructArray](basic-vector-search-with-structarray.md).

4. To review supported data types, nullable behavior, and version-specific limitations, read [StructArray Limits](structarray-limits.md).
