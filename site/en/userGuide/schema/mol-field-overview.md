---
id: mol-field-overview.md
title: "MOL Field Overview"
summary: "Understand how MOL fields represent molecular structures, why fingerprints support similarity search, and how structural matching and similarity search work together."
beta: Milvus 3.0.2+
---

# MOL Field Overview

A molecular library can answer different questions: which molecules contain a benzene ring, and which molecules are similar to phenol? Milvus supports both through molecular structures and fingerprints. A `MOL` field holds the structure for matching; a separate vector field can hold a fingerprint for similarity search.

## What is a MOL field?

A **MOL field** stores molecular structures. You supply each structure as a **SMILES string**, a common text notation that describes atoms and their bond connections. For example, `Oc1ccccc1` represents phenol, a molecule with a benzene ring and an attached hydroxyl group (–OH). See the [Daylight SMILES manual](https://www.daylight.com/dayhtml/doc/theory/theory.smiles.html) for the notation's syntax and examples.

In a collection schema, `MOL` is the data type and `mol` is a field name you choose:

```python
from pymilvus import DataType

schema.add_field(field_name="mol", datatype=DataType.MOL)
```

The following value represents phenol in that field:

```json
{"mol": "Oc1ccccc1"}
```

Milvus interprets this value as a molecular structure, so matching uses atoms and bonds rather than text substrings. When you retrieve the field, Milvus returns a SMILES string.

## Molecular structures and fingerprints

A molecular structure lets Milvus check whether a required structure is present. To rank molecules by similarity, Milvus compares **molecular fingerprints**: binary vectors whose bits summarize structural features of each molecule.

You can generate these fingerprints yourself, or configure Milvus to generate them automatically. The built-in **`MOL_FINGERPRINT` function** connects a `MOL` input field, such as `mol`, to a separate `BINARY_VECTOR` output field, such as `mol_fp`. When you insert a molecule into `mol`, the function generates its fingerprint and stores it in `mol_fp`.

![Phenol is supplied as the SMILES string Oc1ccccc1. In a Milvus collection, the field named mol has data type MOL and holds the structure for matching. An optional MOL_FINGERPRINT function automatically generates a fingerprint in the field named mol_fp, with data type BINARY_VECTOR, for similarity search.](../../../../assets/molecular-data-model.png)

*The same molecule has a structure for matching and a derived fingerprint for similarity search. The fingerprint bits are illustrative.*

For similarity search on the function's output field, you can also supply the reference molecule as SMILES. Milvus generates its fingerprint using the same configuration as the stored fingerprints, so both sides can be compared consistently.

Structural matching uses the `MOL` field directly and does not require the similarity fingerprint or its function.

<div class="alert note">

A collection still requires a primary field and at least one vector field. If you do not use a fingerprint field, include another vector field. [Molecular Search](molecular-search.md#create-a-collection) shows a complete collection setup.

</div>

## Structural matching and similarity search

These retrieval modes answer different questions about the same molecular library:

| Retrieval mode | Example question | What the results mean |
|---|---|---|
| **Structural matching** | Which molecules contain a benzene ring? | Each result satisfies the structural condition. Phenol matches because it contains that ring; ethanol does not. |
| **Similarity search** | Which molecules are most similar to phenol? | Results are ranked by fingerprint similarity to phenol. Their order depends on the features encoded by the fingerprint and the distance metric. |

Structural matching acts as a filter. Similarity search produces a ranking; it does not guarantee that a required structure is present. Different molecules can also share a fingerprint, so even an identical fingerprint does not prove that two molecular structures are identical.

You can combine the two modes. For example, require every result to contain a benzene ring, then rank the qualifying molecules by fingerprint similarity to phenol. The structural condition determines which molecules qualify; the fingerprints determine their order.

## Indexes for molecular retrieval

Indexes accelerate retrieval from the two fields:

| Field | Index | Role and requirement |
|---|---|---|
| `mol` (`MOL`) | `PATTERN` | Accelerates structural filtering by narrowing the candidates before checking their structures. Optional: structural matching also works without it. |
| `mol_fp` (`BINARY_VECTOR`) | A binary vector index | Supports fingerprint similarity search. Required before loading this vector field for search. |

The `PATTERN` index and the similarity fingerprints serve separate purposes. Creating a `PATTERN` index does not generate `mol_fp`. Likewise, the `MOL_FINGERPRINT` function generates vector values but does not create their vector index.

## Next steps

Follow [Molecular Search](molecular-search.md) to create a collection, insert molecules, and try structural matching, similarity search, and combined filtering.

For details, see:

- [Molecular Fingerprints](mol-fingerprint-function.md): fingerprint types, settings, and field configuration.
- [Molecular Operators](molecular-operators.md): structural conditions and their meaning.
- [PATTERN](pattern.md): how the structural index works and how to configure it.
