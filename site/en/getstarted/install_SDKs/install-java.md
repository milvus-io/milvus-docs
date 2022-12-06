---
id: install-java.md
label: Install Java SDK
related_key: SDK
summary: Learn how to install the Java SDK of Milvus.
---

# Install Milvus Java SDK

This topic describes how to install Milvus Java SDK for Milvus.

The current version of Milvus supports SDKs in Python, Node.js, GO, and Java.

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
    <version>{{var.milvus_java_sdk_version}}</version>
</dependency>
```

- Gradle/Grails

```
compile 'io.milvus:milvus-sdk-java:{{var.milvus_java_sdk_version}}'
```

## What's next

Having installed Milvus Java SDK, you can:

- Learn the basic operations of Milvus:
  - [Connect to Milvus server](manage_connection.md)
  - [Create a collection](create_collection.md)
  - [Create a partition](create_partition.md)
  - [Insert data](insert_data.md)
  - [Conduct a vector search](search.md)

- Explore [Milvus Java API reference](/api-reference/java/v{{var.milvus_java_sdk_version}}/About.md)

