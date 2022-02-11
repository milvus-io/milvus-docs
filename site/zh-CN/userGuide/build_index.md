---
id: build_index.md
related_key: create index
summary: Learn how to build an index for vectors in Milvus.
---

# Build an Index

{{fragments/translation_needed.md}}

This topic describes how to build an index for vectors in Milvus. 

Vector indexes are an organizational unit of metadata used to accelerate [vector similarity search](search.md). Without index built on vectors, Milvus will perform a brute-force search by default.

See [Vector Index](index.md) and [Index Selection](index_selection.md) for more information about mechanism and varieties of vector indexes.

<div class="alert note">
<ul>
<li>Current release of Milvus only supports index on vector field. Future releases will support index on scalar field.</li>
<li>By default, Milvus does not index a segment with less than 1,024 rows. To change this parameter, configure <a href="configure_rootcoord.md#rootCoord.minSegmentSizeToEnableIndex"><code>rootCoord.minSegmentSizeToEnableIndex</code></a> in <code>milvus.yaml</code>.</li>
</div>

The following example builds a 1024-cluster IVF_FLAT index with Euclidean distance (L2) as the similarity metrics. You can choose the index and metrics that suit your scenario. See [Similarity Metrics](metric.md) for more information.

## Prepare index parameter

Prepare the index parameters.

{{fragments/multiple_code.md}}

```python
index_params = {
        "metric_type":"L2",
        "index_type":"IVF_FLAT",
        "params":{"nlist":1024}
    }
```

```javascript
const index_params = {
  metric_type: "L2",
  index_type: "IVF_FLAT",
  params: JSON.stringify({ nlist: 1024 }),
};
```

```go
idx, err := entity.NewIndexIvfFlat(   // NewIndex func
    entity.L2,                        // metricType
    1024,                             // ConstructParams
)
if err != nil {
    log.Fatal("fail to create ivf flat index parameter:", err.Error())
}
```

```java
final IndexType INDEX_TYPE = IndexType.IVF_FLAT;   // IndexType
final String INDEX_PARAM = "{\"nlist\":1024}";     // ExtraParam
```

```shell
create index

Collection name (book): book

The name of the field to create an index for (book_intro): book_intro

Index type (FLAT, IVF_FLAT, IVF_SQ8, IVF_PQ, RNSG, HNSW, ANNOY): IVF_FLAT

Index metric type (L2, IP, HAMMING, TANIMOTO): L2

Index params nlist: 1024

Timeout []:
```

<table class="language-python">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
        <th>Options</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>metric_type</code></td>
		<td>Type of metrics used to measure similarity of vectors.</td>
        <td>For floating point vectors:
            <ul>
                <li><code>L2</code> (Euclidean distance)</li>
                <li><code>IP</code> (Inner product)</li>
            </ul>
            For binary vectors:
            <ul>
                <li><code>JACCARD</code> (Jaccard distance)</li>
                <li><code>TANIMOTO</code> (Tanimoto distance)</li>
                <li><code>HAMMING</code> (Hamming distance)</li>
                <li><code>SUPERSTRUCTURE</code> (Superstructure)</li>
                <li><code>SUBSTRUCTURE</code> (Substructure)</li>
            </ul>
        </td>
	</tr>
	<tr>
		<td><code>index_type</code></td>
		<td>Type of index used to accelerate the vector search.</td>
        <td>For floating point vectors:
            <ul>
                <li><code>FLAT</code> (FLAT)</li>
                <li><code>IVF_FLAT</code> (IVF_FLAT)</li>
                <li><code>IVF_SQ8</code> (IVF_SQ8)</li>
                <li><code>IVF_PQ</code> (IVF_PQ)</li>
                <li><code>HNSW</code> (HNSW)</li>
                <li><code>ANNOY</code> (ANNOY)</li>
                <li><code>RHNSW_FLAT</code> (RHNSW_FLAT)</li>
                <li><code>RHNSW_PQ</code> (RHNSW_PQ)</li>
                <li><code>RHNSW_SQ</code> (RHNSW_SQ)</li>
            </ul>
            For binary vectors:
            <ul>
                <li><code>BIN_FLAT</code> (BIN_FLAT)</li>
                <li><code>BIN_IVF_FLAT</code> (BIN_IVF_FLAT)</li>
            </ul>
        </td>
	</tr>
	<tr>
		<td><code>params</code></td>
		<td>Building parameter(s) specific to the index.</td>
        <td>See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	</tbody>
</table>

<table class="language-javascript">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
        <th>Option</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>metric_type</code></td>
		<td>Type of metrics used to measure similarity of vectors.</td>
        <td>For floating point vectors:
            <ul>
                <li><code>L2</code> (Euclidean distance)</li>
                <li><code>IP</code> (Inner product)</li>
            </ul>
            For binary vectors:
            <ul>
                <li><code>JACCARD</code> (Jaccard distance)</li>
                <li><code>TANIMOTO</code> (Tanimoto distance)</li>
                <li><code>HAMMING</code> (Hamming distance)</li>
                <li><code>SUPERSTRUCTURE</code> (Superstructure)</li>
                <li><code>SUBSTRUCTURE</code> (Substructure)</li>
            </ul>
        </td>
	</tr>
	<tr>
		<td><code>index_type</code></td>
		<td>Type of index used to accelerate the vector search.</td>
        <td>For floating point vectors:
            <ul>
                <li><code>FLAT</code> (FLAT)</li>
                <li><code>IVF_FLAT</code> (IVF_FLAT)</li>
                <li><code>IVF_SQ8</code> (IVF_SQ8)</li>
                <li><code>IVF_PQ</code> (IVF_PQ)</li>
                <li><code>HNSW</code> (HNSW)</li>
                <li><code>ANNOY</code> (ANNOY)</li>
                <li><code>RHNSW_FLAT</code> (RHNSW_FLAT)</li>
                <li><code>RHNSW_PQ</code> (RHNSW_PQ)</li>
                <li><code>RHNSW_SQ</code> (RHNSW_SQ)</li>
            </ul>
            For binary vectors:
            <ul>
                <li><code>BIN_FLAT</code> (BIN_FLAT)</li>
                <li><code>BIN_IVF_FLAT</code> (BIN_IVF_FLAT)</li>
            </ul>
        </td>
	</tr>
	<tr>
		<td><code>params</code></td>
		<td>Building parameter(s) specific to the index.</td>
        <td>See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	</tbody>
</table>

<table class="language-go">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
        <th>Options</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>NewIndex func</code></td>
		<td>Function to create entity.Index according to different index types.</td>
        <td>For floating point vectors:
            <ul>
                <li><code>NewIndexFlat</code> (FLAT)</li>
                <li><code>NewIndexIvfFlat</code> (IVF_FLAT)</li>
                <li><code>NewIndexIvfSQ8</code> (IVF_SQ8)</li>
                <li><code>NewIndexIvfPQ</code> (RNSG)</li>
                <li><code>NewIndexRNSG</code> (HNSW)</li>
                <li><code>NewIndexHNSW</code> (HNSW)</li>
                <li><code>NewIndexANNOY</code> (ANNOY)</li>
                <li><code>NewIndexRHNSWFlat</code> (RHNSW_FLAT)</li>
                <li><code>NewIndexRHNSW_PQ</code> (RHNSW_PQ)</li>
                <li><code>NewIndexRHNSW_SQ</code> (RHNSW_SQ)</li>
            </ul>
            For binary vectors:
            <ul>
                <li><code>NewIndexBinFlat</code> (BIN_FLAT)</li>
                <li><code>NewIndexBinIvfFlat</code> (BIN_IVF_FLAT)</li>
            </ul>
        </td>
	</tr>
    <tr>
		<td><code>metricType</code></td>
		<td>Type of metrics used to measure similarity of vectors.</td>
        <td>For floating point vectors:
            <ul>
                <li><code>L2</code> (Euclidean distance)</li>
                <li><code>IP</code> (Inner product)</li>
            </ul>
            For binary vectors:
            <ul>
                <li><code>JACCARD</code> (Jaccard distance)</li>
                <li><code>TANIMOTO</code> (Tanimoto distance)</li>
                <li><code>HAMMING</code> (Hamming distance)</li>
                <li><code>SUPERSTRUCTURE</code> (Superstructure)</li>
                <li><code>SUBSTRUCTURE</code> (Substructure)</li>
            </ul>
        </td>
	</tr>
	<tr>
		<td><code>ConstructParams</code></td>
		<td>Building parameter(s) specific to the index.</td>
        <td>See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	</tbody>
</table>

<table class="language-java">
	<thead>
	<tr>
		<th>Parameter</th>
		<th>Description</th>
        <th>Options</th>
	</tr>
	</thead>
	<tbody>
	<tr>
		<td><code>IndexType</code></td>
		<td>Type of index used to accelerate the vector search.</td>
        <td>For floating point vectors:
            <ul>
                <li><code>FLAT</code> (FLAT)</li>
                <li><code>IVF_FLAT</code> (IVF_FLAT)</li>
                <li><code>IVF_SQ8</code> (IVF_SQ8)</li>
                <li><code>IVF_PQ</code> (IVF_PQ)</li>
                <li><code>HNSW</code> (HNSW)</li>
                <li><code>ANNOY</code> (ANNOY)</li>
                <li><code>RHNSW_FLAT</code> (RHNSW_FLAT)</li>
                <li><code>RHNSW_PQ</code> (RHNSW_PQ)</li>
                <li><code>RHNSW_SQ</code> (RHNSW_SQ)</li>
            </ul>
            For binary vectors:
            <ul>
                <li><code>BIN_FLAT</code> (BIN_FLAT)</li>
                <li><code>BIN_IVF_FLAT</code> (BIN_IVF_FLAT)</li>
            </ul>
        </td>
	</tr>
	<tr>
		<td><code>ExtraParam</code></td>
		<td>Building parameter(s) specific to the index.</td>
        <td>See <a href="index_selection.md">Index Selection</a> for more information.</td>
	</tr>
	</tbody>
</table>

<table class="language-shell">
    <thead>
        <tr>
            <th>Option</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>--help</td>
            <td>Displays help for using the command.</td>
        </tr>
    </tbody>
</table>

## Build index

Build the index by specifying the vector field name and index parameters.

{{fragments/multiple_code.md}}

```python
from pymilvus import Collection
collection = Collection("book")      # Get an existing collection.
collection.create_index(
    field_name="book_intro", 
    index_params=index_params
    )
```

```python
Status(code=0, message='')
```

```javascript
await milvusClient.indexManager.createIndex({
  collection_name: "book",
  field_name: "book_intro",
  extra_params: index_params,
});
```

```go
err = milvusClient.CreateIndex(
    context.Background(),        // ctx
    "book",                      // CollectionName
    "book_intro",                // fieldName
    idx,                         // entity.Index
    false,                       // async
)
if err != nil {
    log.Fatal("fail to create index:", err.Error())
}
```

```java
milvusClient.createIndex(
        CreateIndexParam.newBuilder()
                .withCollectionName("book")
                .withFieldName("book_intro")
                .withIndexType(INDEX_TYPE)
                .withMetricType(MetricType.L2)
                .withExtraParam(INDEX_PARAM)
                .withSyncMode(Boolean.FALSE)
                .build());
```

```shell
# Follow the previous step.
```

<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>field_name</code></td>
            <td>Name of the vector field to build index on.</td>
        </tr>
        <tr>
            <td><code>index_params</code></td>
            <td>Parameters of the index to build.</td>
        </tr>
	</tbody>
</table>


<table class="language-javascript">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>collection_name</code></td>
            <td>Name of the collection to build index in.</td>
        </tr>
        <tr>
            <td><code>field_name</code></td>
            <td>Name of the vector field to build index on.</td>
        </tr>
        <tr>
            <td><code>extra_params</code></td>
            <td>Parameters of the index to build.</td>
        </tr>
	</tbody>
</table>

<table class="language-go">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>ctx</code></td>
            <td>Context to control API invocation process.</td>
        </tr>
        <tr>
            <td><code>CollectionName</code></td>
            <td>Name of the collection to build index on.</td>
        </tr>
        <tr>
            <td><code>fieldName</code></td>
            <td>Name of the vector field to build index on.</td>
        </tr>
        <tr>
            <td><code>entity.Index</code></td>
            <td>Parameters of the index to build.</td>
        </tr>
        <tr>
            <td><code>async</code></td>
            <td>Switch to control sync/async behavior. The deadline of context is not applied in sync building process.</td>
        </tr>
    </tbody>
</table>


## What's next

- Learn more basic operations of Milvus:
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)
  - [Search with Time Travel](timetravel.md)
- Explore API references for Milvus SDKs:
  - [PyMilvus API reference](/api-reference/pymilvus/v{{var.milvus_python_sdk_version}}/tutorial.html)
  - [Node.js API reference](/api-reference/node/v{{var.milvus_node_sdk_version}}/tutorial.html)

