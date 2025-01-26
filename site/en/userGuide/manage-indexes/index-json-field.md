---
id: index-json-field.md
title: JSON Query Optimization
related_key: index-json-field
summary: This article describes how to index JSON fields in Milvus.
---

# JSON Query Optimization

This article describes how JSON fields are indexed and queries on them in Milvus.

## Overview

Fields of the JSON data type are used to store JSON objects. In some scenarios, the performance of JSON-related queries has been suboptimal, especially when dealing with large JSON objects. For example, in dynamic schema use cases, JSON columns can easily balloon in size, with a single row reaching several kilobytes. In such cases, JSON expression queries often suffer from poor performance, with latency easily reaching seconds.

To address this and improve performance, we have designed a new approach to optimize JSON expression queries. Below is an introduction to the basic principles and implementation.

### Current challenges

The existing JSON expression queries in Milvus rely on a brute-force search model, where JSON data is processed row by row. For each query, the entire JSON dataset is scanned. Additionally, during query execution, each row's JSON data must be fully parsed. This means the executor needs to understand all the data in every JSON object, even though most queries only require specific keys or paths. This full parsing process is a major performance bottleneck.

In real-world queries, only a specific key or path in the JSON data is often needed. However, the current approach parses the entire JSON object, resulting in unnecessary overhead.

### Proposed solution

To address these challenges, we introduce a solution that builds inverted indexes for JSON keys, enabling us to minimize the amount of JSON data scanned and parsed.

The core idea is to 

- Skip rows that do not need to be scanned.
- Skip paths within each row that do not need to be parsed.

This solution involves two main processes, namely **Stats Building** and **Search Preprocessing**.

## Stats Building

In the Stats Building process, Milvus asynchronously constructs inverted indexes for all JSON keys in the collection. Instead storeing the actual values of corresponding keys, the inverted indexes store the position of these values within each segment.

Assume that we have two entities in a segment, and the entities have the following data in a JSON field:

```json
{"a": {"b": "milvus", "c": 1}, "d": "database"}
{"a": {"b": "zilliz"}, "e": "database"}
``` 

The inverted index for the JSON field would look like as follows:

- `a.b`: `{(0, 10, 7), (1, 10, 8)}`
- `a.c`: `{(0, 23, 1)}`
- `d`: `{(0, 31, 10)}`
- `e`: `{(1, 25, 10)}`

The inverted index contains the statistics of each JSON path in the data. The index key is the JSON path, and the value is a set of triples, where each triple represents the encoded information about the position of the corresponding value in the segment.

A triple consists of three integers in the following format:

```
(row_id, offset, size)
```

- `row_id`: the ID of the row where the value is located.
- `offset`: the byte offset of the value within the row.
- `size`: the size of the value in bytes.

### Search Preprocessing

