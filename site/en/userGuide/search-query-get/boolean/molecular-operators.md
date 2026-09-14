---
id: molecular-operators.md
title: "Molecular Operators"
summary: "Learn the operators for filtering MOL fields by molecular structure, including their syntax, matching direction, and input requirements."
beta: Milvus 3.0.2+
---

# Molecular Operators

This page describes the operators for filtering `MOL` fields by molecular structure. Use these operators in the `filter` parameter of `query()` to retrieve matching molecules, or of `search()` to restrict similarity search results.

The examples show filter expressions. For collection setup and complete retrieval calls, see [Molecular Search](molecular-search.md).

## MOL_CONTAINS

`MOL_CONTAINS` checks whether the **left molecule contains the right structure**:

```text
MOL_CONTAINS(left, right)
```

- `left`: The molecule to search within. The condition matches only if this molecule contains the structure specified by `right`.
- `right`: The molecular structure to find. This entire structure must be present within `left`.

One side must be a `MOL` field name, and the other must be a quoted SMILES string literal; another field or a filter template placeholder cannot replace the literal. Either side can represent the stored molecule, depending on where you place the field name. Both `MOL_CONTAINS` and `mol_contains` are accepted.

For example, with a `MOL` field named `mol`, the following filter selects stored molecules that contain a benzene ring. Here, `left` is each molecule in `mol`, and `right` is the benzene structure represented by `'c1ccccc1'`:

```python
filter = "MOL_CONTAINS(mol, 'c1ccccc1')"
```

Reversing the arguments changes the matching direction:

| Expression | What it matches |
|---|---|
| `MOL_CONTAINS(mol, 'c1ccccc1')` | Stored molecules that contain the supplied benzene structure |
| `MOL_CONTAINS('c1ccccc1', mol)` | Stored molecules whose structures are contained in the supplied benzene molecule |

The first form finds stored molecules with a required **substructure**. The second finds stored molecules for which the supplied molecule is a **superstructure**. In both forms, the left side contains the right side; changing the argument order changes which side represents the stored molecule.

For a concrete comparison, consider these three stored molecules. The two result columns show the structural matches expected for each argument order:

| Stored molecule | SMILES in `mol` | `MOL_CONTAINS(mol, 'c1ccccc1')` | `MOL_CONTAINS('c1ccccc1', mol)` |
|---|---|---|---|
| Benzene | `c1ccccc1` | Match | Match |
| Phenol | `Oc1ccccc1` | Match | No match |
| Catechol | `Oc1ccccc1O` | Match | No match |

All three contain a benzene ring. Benzene does not contain the additional oxygen atoms in phenol or catechol, so reversing the arguments excludes those two molecules. A structure can contain itself: containment does not require one molecule to be strictly larger than the other.

The operator compares molecular structures, rather than substrings of SMILES text. It does not use a fingerprint similarity threshold. For the distinction between structural matching and fingerprint similarity, see [MOL Field Overview](mol-field-overview.md).

Use valid SMILES, not SMARTS query patterns. Invalid SMILES may cause an error rather than an empty result.

If `mol` is `NULL`, neither `MOL_CONTAINS(mol, 'c1ccccc1')` nor its negation selects that entity. For combining or negating filter conditions, see [Basic Operators](basic-operators.md).

<div class="alert note">

A `PATTERN` index on the `MOL` field can accelerate structural filtering. The operator also works without that index. For index configuration and behavior, see [PATTERN](pattern.md).

</div>
