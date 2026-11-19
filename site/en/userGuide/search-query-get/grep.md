---
id: grep.md
title: "Find Matching Lines with Grep"
summary: "Find the exact lines that match a string or regular expression in stored text and use the results to locate the original source."
---

# Find Matching Lines with Grep

When you investigate a failed request, you may have an error code or a request ID but need the log line that shows what happened. The same problem comes up when you know a function name and need to find where it appears across stored code excerpts.

Grep in {{var.product_name}} brings [`grep`](https://www.gnu.org/software/grep/manual/html_node/Introduction.html)-style line matching to text stored in a collection. Use a metadata filter to narrow the search, for example to a time range or repository, then match a literal string or regular expression against the remaining text. The result includes the matching entities, the exact lines, and their positions within the stored text.

## Limits

- **Input fields.** Grep searches one `VARCHAR` or `TEXT` field defined in the collection schema. For help choosing a field type, see [Choose TEXT or VARCHAR](text.md#choose-text-or-varchar).
- **Matching scope.** Grep evaluates each line independently within its field value. A match cannot span lines or entities. Grep searches stored field values and does not open files by path.
- **Supported options.** Grep uses the [ripgrep](https://github.com/BurntSushi/ripgrep) matching library and accepts a subset of its options. Passing a pattern or file path as a positional argument causes an error. Unsupported options such as `-C` for context lines and `-U` for multiline matching also cause an error.
- **Query combinations.** Grep runs as part of a [Query](get-and-scalar-query.md). Grep queries do not support aggregation, explicit ordering, or query iterators.

## Prepare the text to search

Store the original text in a field and keep any metadata you need to narrow the search or locate the source. If your data is already stored in a loaded collection, [find matching lines](#find-matching-lines) using your own field and collection names.

<details>

<summary><strong>Set up the example collection</strong></summary>

Create a collection using an unused name. The next code block supplies the sample log lines. The `content` field holds the text Grep will search, and `demo_vector` is an auxiliary field for setting up the example collection.

```python
from pymilvus import DataType, MilvusClient

client = MilvusClient(
    uri="{{var.example_endpoint}}",
    token="{{var.example_token}}",
)
collection_name = "logs_by_chunk"

schema = client.create_schema(auto_id=False)
schema.add_field("id", DataType.INT64, is_primary=True)
schema.add_field("host", DataType.VARCHAR, max_length=64)
schema.add_field("source_file", DataType.VARCHAR, max_length=256)
# highlight-start
# Record the source file line where this fragment begins.
schema.add_field("source_start_line", DataType.INT64)
# Store the text that Grep will search.
schema.add_field("content", DataType.VARCHAR, max_length=1024)
# highlight-end
schema.add_field("demo_vector", DataType.FLOAT_VECTOR, dim=2)

index_params = client.prepare_index_params()
index_params.add_index("demo_vector", index_type="FLAT", metric_type="L2")
client.create_collection(
    collection_name=collection_name,
    schema=schema,
    index_params=index_params,
    consistency_level="Strong",
)
```

In the code below, the three sample lines represent lines 41 through 43 of `payment.log`. Insert them as one entity and preserve the line breaks in `content`. The example stores `41` in `source_start_line` because the first line of the fragment came from line 41 of the file. Grep searches from the first line of `content`. Use `source_start_line` after the query to locate a match in the source file.

Load the collection after inserting the sample data so you can query it.

```python
lines = [
    "INFO request started",
    "ERROR_TIMEOUT order=4182",
    "INFO retry scheduled",
]
source = {
    "host": "payment-01",
    "source_file": "payment.log",
    "demo_vector": [0.0, 1.0],
}
client.insert(
    collection_name=collection_name,
    data=[
        {
            **source,
            "id": 201,
            # highlight-start
            "source_start_line": 41,
            # Preserve line breaks so Grep can return each matching line.
            "content": "\n".join(lines),
            # highlight-end
        }
    ],
)
client.load_collection(collection_name=collection_name)
```

</details>

## Find matching lines

After loading the example collection, find the line containing `ERROR_TIMEOUT` in `payment.log` on the host `payment-01`.

```python
log_filter = 'host == "payment-01" and source_file == "payment.log"'
output_fields = ["id", "source_file", "source_start_line"]

results = client.grep(
    collection_name=collection_name,
    # highlight-start
    # Search the original text stored in this field.
    text_field="content",
    # Match the literal error code.
    args="-F -e ERROR_TIMEOUT",
    # Search only entities from this host and file.
    filter=log_filter,
    # highlight-end
    output_fields=output_fields,
    limit=10,
)
```

Pass the matching options and pattern together as one string in `args`. In this example, `-e` specifies the pattern and `-F` matches it as literal text. `limit=10` returns up to 10 matching entities. For more ways to write `args`, see [Matching options and result limits](#matching-options-and-result-limits).

To query your own data, use a connected client and a loaded collection. Replace the collection and field names, including the fields in `output_fields`. Adjust `filter` to narrow the search or omit it to search all entities in the collection.

<details>

<summary><strong>Matching options and result limits</strong></summary>

<a id="matching-options-and-result-limits"></a>

**Write the `args` string**

- **Specify a pattern.** Put `-e` or `--regexp` before each pattern.
- **Quote patterns with spaces.** In the first example below, the outer double quotes delimit the Python string. The inner single quotes keep `request started` together as one pattern.
- **Preserve regex escapes.** In Python, use a raw string (`r"..."`) to pass backslashes such as `\d` and `\b` to Grep. In an ordinary Python string, write them as `\\d` and `\\b`.
- **Match any of several patterns.** Repeat `-e` for each pattern in the same `args` string. Options such as `-F` and `-i` apply to all the patterns in that request.

| To find | Python value for `args` |
| --- | --- |
| The literal text `request started` | `"-F -e 'request started'"` |
| `ERROR_TIMEOUT` regardless of case | `"-F -i -e ERROR_TIMEOUT"` |
| `order=` followed by one or more digits | `r"-e 'order=\d+'"` |
| Either `ERROR_TIMEOUT` or `CONNECTION_RESET` | `"-F -e ERROR_TIMEOUT -e CONNECTION_RESET"` |

Grep uses case-sensitive regular expressions by default. Add `-F` for literal matching, `-i` to ignore case, or `-s` to explicitly match case. Use either `-w` for whole words or `-x` for whole lines.

**Limit matching lines per entity.** If an entity has two matching lines, a request with `limit=1` can still return both lines in that entity's `matches`. If your deployment supports `-m` (`--max-count`), add `-m 1` to `args` to retain only the first matching line per entity. For example, `args="-F -m 1 -e ERROR_TIMEOUT"` keeps the first line containing that error code in each returned entity.

</details>

## Read the results

The sample query returns entity `201` and one entry in `matches`.

```json
[
  {
    "id": 201,
    "source_file": "payment.log",
    "source_start_line": 41,
    "matches": [
      {
        "content": "ERROR_TIMEOUT order=4182",
        "line_number": 2,
        "line_start_offset": 21,
        "starts": [0],
        "ends": [13]
      }
    ]
  }
]
```

The entity's `id` identifies the stored log fragment. The `line_number` starts at 1 for each field value, so `2` means the second line of this fragment. Because the fragment preserves consecutive lines from the source file, you can calculate the original line as `source_start_line + line_number - 1`.

```python
for entity in results:
    for match in entity["matches"]:
        source_line = entity["source_start_line"] + match["line_number"] - 1
        print(f"{entity['source_file']}:{source_line}: {match['content']}")
```

```plaintext
payment.log:42: ERROR_TIMEOUT order=4182
```

To highlight the exact match, use `starts` and `ends` as paired UTF-8 byte offsets within the returned line. The start is inclusive and the end is exclusive. In this example, bytes `[0, 13)` contain `ERROR_TIMEOUT`. To locate those bytes in the stored fragment, add `line_start_offset`, the byte offset of the start of the line within the field value.

<details>

<summary><strong>Store one log line per entity</strong></summary>

Both layouts store the same three log lines. In the main example, the error is the second line of a three-line entity. If you store each line as its own entity, the error is the only line in the matching entity, so Grep reports `line_number=1`.

| Storage layout | Entities written | Matching entity ID | `line_number` | Source file line |
| --- | ---: | ---: | ---: | ---: |
| One entity for the three-line fragment | 1 | `201` | `2` | `42` |
| One entity per log line | 3 | `102` | `1` | `42` |

To try this layout, reuse the schema, index parameters, and log data from the main example. Insert each line into a separate entity and store its original file line in `source_start_line`.

```python
line_collection_name = "logs_by_line"
client.create_collection(
    collection_name=line_collection_name,
    schema=schema,
    index_params=index_params,
    consistency_level="Strong",
)
rows_by_line = [
    {**source, "id": 101 + i, "source_start_line": 41 + i, "content": line}
    for i, line in enumerate(lines)
]
client.insert(collection_name=line_collection_name, data=rows_by_line)
client.load_collection(collection_name=line_collection_name)

line_results = client.grep(
    collection_name=line_collection_name,
    text_field="content",
    args="-F -e ERROR_TIMEOUT",
    filter=log_filter,
    output_fields=output_fields,
    limit=10,
)

for entity in line_results:
    for match in entity["matches"]:
        print(f"Entity {entity['id']}, line {match['line_number']}: {match['content']}")
```

```plaintext
Entity 102, line 1: ERROR_TIMEOUT order=4182
```

For entity `102`, the source line calculation is `42 + 1 - 1 = 42`.

</details>
