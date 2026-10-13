---
id: pattern.md
title: "PATTERN"
summary: "Use a PATTERN index on a MOL field to accelerate structural filtering, understand candidate screening, and configure the index fingerprint length."
beta: Milvus 3.0.2+
---

# PATTERN

The `PATTERN` index accelerates filtering by molecular structure on `MOL` fields. It uses RDKit's [Pattern Fingerprints](https://www.rdkit.org/docs/RDKit_Book.html#pattern-fingerprints), binary summaries of molecular features, to quickly exclude molecules that cannot match a filter.

<div class="alert note">

Structural filtering works without a `PATTERN` index. Without it, Milvus checks molecular structures directly, which can be costly when many molecules need to be examined. For collection setup and a complete retrieval workflow, see [Molecular Search](molecular-search.md).

</div>

## How it works

To determine whether one molecule contains another's structure, Milvus compares their atoms, bonds, and connections. `PATTERN` reduces this work by screening fingerprints first, then checking the structures of the remaining candidates. This filtering step applies to both `query()` and `search()` requests with a molecular filter.

The following example searches for molecules containing a benzene ring in a library of benzene, phenol, catechol, and ethanol:

![Four molecules, each labeled with its SMILES input, contribute fingerprints to the PATTERN index on mol. A benzene-ring filter screens out ethanol, then checks the structures of benzene, phenol and catechol. These three match the filter. The displayed fingerprints show eight selected bit positions; screening uses the full fingerprints.](../../../../../assets/molecular-pattern-screening.png)

*Example calculated with RDKit. Only eight bit positions are shown; screening uses the full fingerprints.*

### Phase 1: Build the index

You supply molecules as SMILES strings when inserting data into `mol`. Each card in the figure shows a molecule's structure and its SMILES input. You create the `PATTERN` index on the field; Milvus generates a Pattern fingerprint for each indexed molecule and stores these fingerprints together in the index.

To generate each fingerprint, RDKit identifies features in the molecular structure and maps them to bit positions. Those positions are set to `1`; the others remain `0`. Different features can map to the same position, so the bits are not a one-to-one checklist of chemical features.

The figure shows the same eight positions for every fingerprint. Matching excerpts do not mean the full fingerprints are identical. Milvus retains the molecular structures in `mol` for the subsequent structure checks; no `MOL_FINGERPRINT` function or separate `BINARY_VECTOR` field is needed for this index.

### Phase 2: Apply a molecular filter

For the filter `MOL_CONTAINS(mol, 'c1ccccc1')`, Milvus:

1. **Generates the filter fingerprint.** The benzene molecule supplied as SMILES in the filter is converted to a Pattern fingerprint with the same length as the index fingerprints.
2. **Screens candidates.** Every bit set to `1` in the filter fingerprint must also be set to `1` in a candidate's fingerprint. Ethanol fails this check; benzene, phenol, and catechol remain as candidates.
3. **Checks actual structures.** Milvus checks each candidate's atoms, bonds, and connections for the required benzene ring. All three candidates in this example match the filter. This checks whether the required structure is present, not whether the molecules are identical.

Because fingerprints are compressed representations, passing the screen does not prove that a molecule contains the query structure. The final structure check removes any candidates that do not match.

What happens next depends on the request:

- **`query()`** returns entities that match the filter, subject to the requested result limit. It does not rank them by molecular similarity.
- **`search()` with standard filtering** performs similarity search among entities that match the filter. For molecular similarity search on `mol_fp`, Milvus compares the separate fingerprint vectors using the configured metric, such as `JACCARD`, and returns the closest matches. `PATTERN` accelerates the structural filtering step; the vector index on `mol_fp` serves the similarity search. A similarity search without a molecular filter does not use `PATTERN`.

For example, you can filter for molecules containing a benzene ring, then rank the matches by similarity to phenol. Benzene supplies the filter's Pattern fingerprint; phenol supplies the similarity-search fingerprint through the configured `MOL_FINGERPRINT` function. This ranking compares fingerprint vectors rather than checking atoms and bonds again. See [Molecular Search](molecular-search.md#combine-structure-and-similarity) for the complete example.

For the reverse expression, `MOL_CONTAINS('c1ccccc1', mol)`, Milvus reverses the containment direction in both screening and structure checking. See [Molecular Operators](molecular-operators.md) for argument order and matching rules.

## Create a PATTERN index

The following example creates `mol_pattern` on an unindexed `MOL` field named `mol`. It assumes a connected `client` and an existing collection named `molecular_library`; see [Molecular Search](molecular-search.md#create-a-collection) for collection setup.

```python
index_params = client.prepare_index_params()

index_params.add_index(
    field_name="mol",  # The MOL field to index.
    # highlight-start
    index_type="PATTERN",
    index_name="mol_pattern",
    params={"n_bit": 2048},  # Pattern fingerprint length, in bits.
    # highlight-end
)

client.create_index(
    collection_name="molecular_library",
    index_params=index_params,
)
```

`PATTERN` has one index-specific build parameter, `n_bit`. You can omit `params` to use its default value:

| Parameter | What it controls | Default | Accepted range |
|---|---|---|---|
| `n_bit` | Length, in bits, of each Pattern fingerprint stored in the index | `2048` | Integer from `64` to `4096` |

Query fingerprints use the length recorded in the index, so you do not set `n_bit` again in each query.

Longer fingerprints require more storage. Screening effectiveness and query speed depend on the molecules and queries, so increasing `n_bit` does not guarantee faster queries.

For fingerprint similarity search, `MOL_FINGERPRINT` uses a separate `fingerprint_size` and output field `dim`. Neither needs to match the PATTERN index's `n_bit`; see [Molecular Fingerprints](mol-fingerprint-function.md).

Load the collection before querying; see [Molecular Search](molecular-search.md#create-indexes-and-load-the-collection) for the complete index and loading setup.

<div class="alert note">

Milvus automatically uses an available `PATTERN` index for `MOL_CONTAINS` filters on the indexed field, in both `query()` and `search()`. You do not need to name the index in the filter or supply PATTERN-specific search parameters.

</div>

## Drop an index

When you no longer need the index to accelerate structural filtering, drop it to free the resources it uses. If the collection is loaded, release it first, then drop the index using the name supplied during creation:

```python
client.release_collection(collection_name="molecular_library")

client.drop_index(
    collection_name="molecular_library",
    index_name="mol_pattern",
)
```

Dropping the index retains the molecular data. After loading the collection again, structural filtering remains available without the `PATTERN` acceleration.
