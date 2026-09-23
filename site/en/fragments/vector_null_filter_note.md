<div class="alert note">

Starting in Milvus 3.0.3, you can use `IS NULL` and `IS NOT NULL` in query and search filters on ordinary vector fields to select entities whose vector field is NULL or non-NULL, respectively.

To find entities whose `embedding` field is NULL, use `query()` with the filter `embedding IS NULL`. This filter is also valid in `search()`. However, searching on `embedding` with this filter returns no hits: entities without an `embedding` value have no vector to compare with the query vector.

For supported types, syntax, and examples, see [IS NULL and IS NOT NULL operators](basic-operators.md#IS-NULL-and-IS-NOT-NULL-operators).

</div>
