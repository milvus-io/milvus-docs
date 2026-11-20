---
id: grep.md
title: "Find Matching Lines with Grep"
summary: "Find the exact lines that match a string or regular expression in stored text and use the results to locate the original source."
---

# Find Matching Lines with Grep

You may know what text to search for and still need to find the line where it appears. In service logs, an error code or request ID can help you locate the line that records a failed request. In source code, a function's old name can help you find references to update after a rename.

Grep in {{var.product_name}} finds matching lines in stored logs or source code, much like the [`grep`](https://www.gnu.org/software/grep/manual/html_node/Introduction.html) command. A metadata filter can narrow the search to a service or repository. Grep matches a literal string or regular expression against the text. It returns the matching entities with each matching line and its position in the stored text.

## Limits

- **Input fields.** Grep searches one `VARCHAR` or `TEXT` field defined in the collection schema. For help choosing a field type, see [Choose TEXT or VARCHAR](text.md#choose-text-or-varchar).
- **Matching scope.** Grep matches one line at a time. A match cannot continue onto the next line or into another entity.
- **Supported options.** Grep uses the [ripgrep](https://github.com/BurntSushi/ripgrep) matching library and supports a subset of ripgrep's command-line options. See [Matching options and result limits](#matching-options-and-result-limits) for the supported options and examples.
- **Query combinations.** The `grep()` method runs a [Query](get-and-scalar-query.md) with text matching. If you supply a filter, the query applies it before Grep searches the selected text field. Grep queries do not support Query Aggregation, [`ORDER BY`](get-and-scalar-query.md#Sort-Query-Results), or Query Iterator.

## Prepare the text to search

Store the original text in a field. Keep the metadata you need to narrow the search or locate the source. If your data is in a loaded collection, use your own field and collection names to [find matching lines](#find-matching-lines).

<details>

<summary><strong>Set up the example collection</strong></summary>

Create a collection with an unused name. The insert example below supplies the sample log lines. The `content` field holds the text that Grep searches. The example uses `demo_vector` as an auxiliary field for the collection.

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

In the code below, the three sample lines represent lines 41 through 43 of `payment.log`. Keep the line breaks in `content`. Insert the three lines as one entity.

Set `source_start_line` to `41` to record where the fragment starts in the file. Grep searches from the first line of `content`. Use `source_start_line` after the query to locate a match in the source file.

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
    # Put -e before the pattern you want to find.
    # Use -F to match the pattern as plain text.
    args="-F -e ERROR_TIMEOUT",
    # Search only entities from this host and file.
    filter=log_filter,
    # highlight-end
    output_fields=output_fields,
    # Return up to 10 matching entities.
    limit=10,
)
```

For more examples, see [Matching options and result limits](#matching-options-and-result-limits).

To query your own data, use a connected client and a loaded collection. Replace the collection and field names, including the fields in `output_fields`. To narrow the search, adjust `filter`. To search all entities in the collection, omit `filter`.

<details>

<summary><strong>Matching options and result limits</strong></summary>

<a id="matching-options-and-result-limits"></a>

**Build the `args` string**

Pass the matching options and patterns in one string. Separate them with spaces.

- **`-e` (`--regexp`).** Put this option before each search pattern. Include at least one pattern. Passing a pattern or file path as a positional argument causes an error. Grep returns a line if it matches any of the patterns. By default, Grep treats each pattern as a case-sensitive regular expression.
- **`-F` (`--fixed-strings`).** Use uppercase `-F` to match all patterns as plain text.
- **`-i` (`--ignore-case`) or `-s` (`--case-sensitive`).** Use `-i` to ignore case or `-s` to match case. If you pass both, the last one takes effect.
- **`-w` (`--word-regexp`) or `-x` (`--line-regexp`).** Use `-w` to match whole words or `-x` to match the entire line. Grep returns an error if you combine these options.

**Choose a result limit**

- **`limit` on the `grep()` call.** Set the maximum number of matching entities to return. An entity can still have several lines in `matches`.
- **`-m` (`--max-count`) inside `args`.** If your deployment supports this option, pass a non-negative integer to return up to that many matching lines per entity. With `-m 0`, Grep returns no entities.

**Examples**

The examples show the contents of `args` as Grep receives them. The last example also sets `limit` on the `grep()` call. If a pattern contains spaces, put single or double quotes around the pattern inside `args`. In SDK code, follow your language's string rules to preserve those quotes and regex backslashes such as `\d` and `\b`.

| Goal | What to pass |
| --- | --- |
| Text such as `v1.2` or `v1-2` (`.` matches any character on the line) | `-e v1.2` |
| The literal text `v1.2` (`.` matches a period) | `-F -e v1.2` |
| The literal phrase `request started` | `-F -e 'request started'` or `-F -e "request started"` |
| `ERROR_TIMEOUT` regardless of case | `-F -i -e ERROR_TIMEOUT` |
| `order=` followed by one or more digits | `-e 'order=\d+'` |
| Either `ERROR_TIMEOUT` or `CONNECTION_RESET` | `-F -e ERROR_TIMEOUT -e CONNECTION_RESET` |
| The whole word `timeout`, as in `request timeout` | `-F -w -e timeout` |
| A line consisting entirely of `timeout` | `-F -x -e timeout` |
| Return the first line containing `ERROR_TIMEOUT` from each of up to 10 matching entities | Set `limit=10` on the call and pass `-F -m 1 -e ERROR_TIMEOUT` in `args`. |

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

The entity's `id` identifies the log fragment. Grep numbers the lines in each field value starting at 1. In this example, `line_number=2` identifies the second line of the fragment. The fragment preserves consecutive lines from the source file. Calculate the source line as `source_start_line + line_number - 1`.

```python
for entity in results:
    for match in entity["matches"]:
        source_line = entity["source_start_line"] + match["line_number"] - 1
        print(f"{entity['source_file']}:{source_line}: {match['content']}")
```

```plaintext
payment.log:42: ERROR_TIMEOUT order=4182
```

To highlight the match, use `starts` and `ends` as paired UTF-8 byte offsets within the returned line. The start is inclusive. The end is exclusive. In this example, bytes `[0, 13)` contain `ERROR_TIMEOUT`. To locate those bytes in the stored fragment, add `line_start_offset` to both offsets. `line_start_offset` points to the first byte of the returned line within the field value.

<details>

<summary><strong>Store one log line per entity</strong></summary>

Both layouts store the same three log lines. In the main example, the error is the second line of a three-line entity. If you store each line as a separate entity, the matching entity contains only the error line. Grep therefore reports `line_number=1`.

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
