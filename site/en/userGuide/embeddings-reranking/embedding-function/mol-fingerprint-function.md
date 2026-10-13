---
id: mol-fingerprint-function.md
title: "Molecular Fingerprints"
summary: "Compare molecular fingerprint types, configure structural coverage and fingerprint length, and understand how MOL_FINGERPRINT generates vectors for insertion and search."
beta: Milvus 3.0.2+
---

# Molecular Fingerprints

The `MOL_FINGERPRINT` function converts molecular structures into binary fingerprints for similarity search. The fingerprint type and its settings determine which structural features the fingerprint represents and how many bits it uses.

This page describes the available types, their settings, and the field configuration they require. For the relationship between molecular structures and fingerprints, see [MOL Field Overview](mol-field-overview.md). For a complete insertion and search workflow, see [Molecular Search](molecular-search.md).

Choose a fingerprint type, then configure the structural features it covers and its length. These choices go in the `MOL_FINGERPRINT` function's `params`. For example, a Morgan configuration looks like this:

```python
params = {
    "fingerprint_type": "morgan",  # Type
    "radius": "2",                # Structural coverage
    "fingerprint_size": "2048",    # Length in bits
}
```

This fragment shows the fingerprint settings. The full field and function setup appears under [Field configuration](#field-configuration).

## Fingerprint types

Milvus uses the [RDKit chemistry toolkit](https://rdkit.org/docs/RDKit_Book.html#additional-information-about-the-fingerprints) to generate molecular fingerprints. It supports three fingerprint types from this toolkit: `morgan`, `rdkit`, and `maccs`. Set `fingerprint_type` to select one; the default is `morgan`.

| Type | Structural features represented | Settings that control the fingerprint |
|---|---|---|
| `morgan` | Atom-centered neighborhoods, expanded through successive layers of bonds | `radius` controls neighborhood size; `fingerprint_size` controls output length |
| `rdkit` (topological fingerprint) | Molecular subgraphs, including branched structures, within a range of bond counts | `min_path` and `max_path` control subgraph size; `fingerprint_size` controls output length |
| `maccs` | The presence of a predefined set of structural features, known as MACCS keys | Fixed feature set and output length; no radius or path-length settings |

<div class="alert note">

Similarity search requires the stored molecules and the query molecule to use the same fingerprint type and settings. When you search the function's output field with a SMILES string, Milvus applies the same configured function used for insertion, so this consistency is handled automatically.

</div>

For algorithm details, see the [RDKit fingerprint descriptions](https://rdkit.org/docs/RDKit_Book.html#additional-information-about-the-fingerprints), [Morgan fingerprint reference](https://www.rdkit.org/docs/cppapi/namespaceRDKit_1_1MorganFingerprints.html), and [MACCS fingerprint reference](https://www.rdkit.org/docs/cppapi/namespaceRDKit_1_1MACCSFingerprints.html). The selected type also determines which settings you can adjust. The following section describes these settings and their defaults in Milvus.

## Fingerprint settings

The available settings depend on `fingerprint_type`. **Morgan** and **RDKit** let you adjust structural coverage and fingerprint length. **MACCS** has a fixed feature set and length, so set only `fingerprint_type="maccs"`; no additional fingerprint settings are needed.

### Structural coverage

Coverage settings determine which parts of a molecule contribute features to the fingerprint. Each type uses a different approach:

| Type | Setting | What it controls | Default and constraint |
|---|---|---|---|
| `morgan` | `radius` | How far each atom-centered neighborhood extends, measured in bonds from the center atom | Default: `2`; must be at least `0` |
| `rdkit` | `min_path` | Minimum number of bonds in a molecular subgraph included in the fingerprint | Default: `1`; must be at least `1` |
| `rdkit` | `max_path` | Maximum number of bonds in an included subgraph; subgraphs can be branched as well as linear | Default: `7`; must be at least `min_path` |
| `maccs` | None | Uses a predefined set of structural keys | Fixed; omit `radius`, `min_path`, and `max_path` |

For example, increasing the Morgan `radius` from `2` to `3` includes neighborhoods extending one bond further where available. For RDKit, reducing `max_path` from `7` to `5` excludes subgraphs containing six or seven bonds, as in this alternative `params` fragment:

```python
params = {
    "fingerprint_type": "rdkit",
    "fingerprint_size": "2048",
    # highlight-start
    "min_path": "1",
    "max_path": "5",
    # highlight-end
}
```

Pass this dictionary as the function's `params` when configuring a new collection. For more on structural coverage, see RDKit's [Morgan fingerprint explanation](https://www.rdkit.org/docs/GettingStartedInPython.html#morgan-fingerprints-circular-fingerprints) and [RDKit fingerprint options](https://rdkit.org/docs/RDKit_Book.html#fingerprint-specific-options).

### Fingerprint length

Length is the number of bits used to represent the selected features. Its configuration also depends on the type:

| Type | Length configuration |
|---|---|
| `morgan` or `rdkit` | Set `fingerprint_size` to a positive integer. The default is `2048` bits. |
| `maccs` | Fixed at `168` bits in Milvus. Omit `fingerprint_size`; it cannot change the MACCS output length. |

Increasing the length does not expand structural coverage, and a longer fingerprint does not necessarily produce more useful similarity results. The output vector field's `dim` must match this length and meet the dimension constraints below.

## Field configuration

Once you have chosen the fingerprint type and settings, configure the fields that supply the molecular structures and store the generated fingerprints. The function connects exactly one `MOL` input field to one `BINARY_VECTOR` output field. Define both fields and add the function to the schema before creating the collection.

This fragment extends an existing `schema` created with `client.create_schema()`. It shows the molecular fields and function; the primary field and collection creation are covered in [Molecular Search](molecular-search.md#create-a-collection).

```python
from pymilvus import DataType, Function, FunctionType

schema.add_field(field_name="mol", datatype=DataType.MOL)

# Store the fingerprints generated from mol.
schema.add_field(
    field_name="mol_fp",
    datatype=DataType.BINARY_VECTOR,
    # highlight-next-line
    dim=2048,  # Must match fingerprint_size below.
)

schema.add_function(
    Function(
        name="mol_fingerprint",
        # highlight-start
        function_type=FunctionType.MOL_FINGERPRINT,
        input_field_names=["mol"],      # Read molecular structures.
        output_field_names=["mol_fp"],  # Write generated fingerprints.
        # highlight-end
        params={
            "fingerprint_type": "morgan",
            "fingerprint_size": "2048",
            "radius": "2",
        },
    )
)
```

The function settings above are passed as string values, while the vector field's `dim` is an integer. For an RDKit configuration, replace the function's `params` dictionary with the RDKit example above; its `fingerprint_size` is also `2048`, so the output dimension remains `2048`.

The output field must satisfy these requirements:

| Fingerprint type | Required output dimension |
|---|---|
| `morgan` or `rdkit` | Equal to `fingerprint_size`; a positive multiple of `8` within the server's vector dimension limit |
| `maccs` | Exactly `168` |

With the default server dimension limit, binary vector dimensions can range from `8` through `262144` bits, in multiples of `8`. A dimension that does not match the generated fingerprint size is an invalid function configuration. For example, `fingerprint_size="2048"` cannot be paired with `dim=1024`.

<details>

<summary>MACCS field configuration</summary>

For a MACCS-based collection, use the following alternative in a new schema that already defines a `MOL` field named `mol`. The imports are the same as above. Use this instead of the Morgan output field and function configuration; it is not an update to an existing collection.

```python
schema.add_field(
    field_name="mol_fp",
    datatype=DataType.BINARY_VECTOR,
    # highlight-next-line
    dim=168,  # MACCS has a fixed output dimension in Milvus.
)

schema.add_function(
    Function(
        name="mol_fingerprint",
        function_type=FunctionType.MOL_FINGERPRINT,
        input_field_names=["mol"],
        output_field_names=["mol_fp"],
        # highlight-next-line
        params={"fingerprint_type": "maccs"},
    )
)
```

</details>

## Generation during insertion and search

The configured function serves both stored molecules and reference molecules used for search:

| Operation | What you provide | What Milvus generates |
|---|---|---|
| Insertion | A SMILES string in the `mol` field of each entity | A fingerprint stored in `mol_fp` using the configured type and settings |
| Search on `mol_fp` | Reference molecules as SMILES strings in the search input | Query fingerprints generated with the same function configuration and compared with the stored fingerprints |

Do not supply `mol_fp` values when inserting entities: it is the function's generated output field. For a SMILES search, target `mol_fp` rather than `mol`; the search input supplies the reference molecule, and the field binding selects the fingerprint configuration.

Fingerprint generation and distance measurement have separate settings. The function defines the feature representation. The vector index defines the metric used to compare those representations, such as `JACCARD`; `metric_type` is not a fingerprint function setting.

For complete index configuration and retrieval examples, see [Molecular Search](molecular-search.md#create-indexes-and-load-the-collection).
