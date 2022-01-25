---
id: install-go.md
label: Install GO SDK
related_key: SDK
order: 2
group: install-pymilvus.md
summary: Learn how to install the GO SDK of Milvus.
---

# Install Milvus SDK

This topic describes how to install Milvus SDK for Milvus.

Current version of Milvus supports SDKs in Python, Node.js, GO, and Java.

{{tab}}

## Requirement

GO (1.15 or later) is required.

## Install Milvus GO SDK

Install the Milvus GO SDK and dependencies via `go get`.

```bash
$ go get -u github.com/milvus-io/milvus-sdk-go/v2
```

## What's next

Having installed Milvus GO SDK, you can:

- Learn the basic operations of Milvus:
  - [Connect to Milvus server](manage_connection.md)
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)

- Explore [Milvus GO API reference](/api-reference/go/v{{var.milvus_go_sdk_version}}/tutorial.html)

