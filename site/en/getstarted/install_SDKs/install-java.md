---
id: install-java.md
label: Install Java SDK
related_key: SDK
order: 3
group: install-pymilvus.md
summary: Learn how to install the Java SDK of Milvus.
---

# Install Milvus SDK

This topic describes how to install Milvus SDK for Milvus.

Current version of Milvus supports SDKs in Python, Node.js, GO, and Java.

{{tab}}

## Requirement

- Java (8 or later)
- Apache Maven or Gradle/Grails

## Install Milvus Java SDK

Run the following command to install Milvus Java SDK.

- Apache Maven

```xml
<dependency>
    <groupId>io.milvus</groupId>
    <artifactId>milvus-sdk-java</artifactId>
    <version>2.0.0</version>
</dependency>
```

- Gradle/Grails

```
compile 'io.milvus:milvus-sdk-java:2.0.0'
```

## What's next

Having installed Milvus Java SDK, you can:

- Learn the basic operations of Milvus:
  - [Connect to Milvus server](manage_connection.md)
  - [Conduct a vector search](search.md)
  - [Conduct a hybrid search](hybridsearch.md)

- Explore [Milvus Java API reference](/api-reference/node/v{{var.milvus_java_sdk_version}}/tutorial.html)

