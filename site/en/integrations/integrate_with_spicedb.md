---
id: integrate_with_spicedb.md
summary: Learn how to build a permission-aware RAG system using Milvus for vector search and SpiceDB for fine-grained, Zanzibar-inspired access control.
title: Permission-Aware RAG with Milvus and SpiceDB
---

# Permission-Aware RAG with Milvus and SpiceDB

Most RAG systems treat retrieval as a relevance problem where a user types a query, gets the closest chunks back, and an LLM generates the answer from the data that is returned. However, this ignores a serious risk: **information leakage**. If different users have different levels of access to data, as they do in most real-world systems, your RAG pipeline must enforce those access boundaries. In fact, OWASP lists Sensitive Information Disclosure, Excessive Agency, and Vector and Embedding Weaknesses in their list of [Top 10 Risks for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

That's where fine-grained access control comes in. Instead of trusting the RAG system to "just do the right thing," you can integrate an authorization layer that determines which resources a given identity can access. This guide explores how to achieve that using [SpiceDB](https://authzed.com/spicedb), an open-source, Zanzibar-inspired permission system, together with Milvus.

## Background

### Google Zanzibar

Google Zanzibar is the internal authorization system that manages permissions across all of Google's products and services. Think of it as the system that decides whether you can view a shared Google Doc, or edit the description of a YouTube video. Compared to traditional authorization methods such as Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC), Zanzibar utilizes Relationship-Based Access Control (ReBAC) where permissions are determined by relationships between users and resources.

Zanzibar was built for requirements including:

- Low-latency at Google-scale
- High-throughput authorization checks
- Global consistency of relationship data
- Hierarchical permission models (for example, files in folders, people in groups)

RAG systems and Agentic AI typically share these requirements, which makes a Zanzibar-like system an ideal candidate for your permission layer.

### SpiceDB

SpiceDB is an open-source authorization system for fine-grained permission checks at scale, inspired by Google Zanzibar. It's used by companies such as OpenAI, Workday, and Turo.

Together with Milvus, you can build a retrieval pipeline that respects your permission model. This guide covers two strategies for combining them:

- **Pre-filter**: Ask SpiceDB which documents a user can access *before* the vector search, then restrict Milvus to that set.
- **Post-filter**: Retrieve candidates from Milvus by relevance first, then batch-verify permissions with SpiceDB.

### How it works

SpiceDB stores access relationships as a graph, where nodes represent entities (users, groups, documents) and edges represent relationships (such as "viewer," "editor," or "owner"). Authorization logic reduces to asking a single question:

> Is this `actor` allowed to perform this `action` on this `resource`?

In SpiceDB parlance, the actor and resource are both Objects, and the action is a Permission.

Here's a Google Docs-style example where a user can be either a `reader` or a `writer` of a document. A reader can only `read` the document, whereas a writer can both `read` and `edit` it:

```
definition user {}

definition document {
    relation reader: user
    relation writer: user

    permission edit = writer
    permission read = reader + edit
}
```

This schema is intentionally minimal. In a real system, you'd model groups, organizational roles, folder-level inheritance, or resource hierarchies — all of which SpiceDB handles. The sample app later in this guide contains a more complex model. The retrieval integration pattern works regardless of schema complexity; only the relationship writes change.

When a user requests access to a document, SpiceDB answers questions like:

> "Can `user:alice` perform `read` on `document:doc1`?"

It evaluates the relationship graph, enabling real-time authorization checks at massive scale.

## How the demo is built

This demo showcases an Agentic RAG system where a user asks a query and retrieves information based on the documents they're authorized to access. The "agentic" part refers to an AI agent that reasons about whether more data should be retrieved, but does **not** — and should not — reason about **whether** authorization is required.

The system has three components: **Milvus** for document storage and retrieval, **SpiceDB** for authorization, and a **LangGraph** agent that orchestrates the flow. The demo also uses OpenAI for embeddings and LLM responses.

![System architecture: Milvus, SpiceDB, and LangGraph agent]({{images.assets/spicedb-architecture.png "Milvus, SpiceDB, and LangGraph system architecture"}})

### Who can see what

The demo corpus spans four departments: engineering, sales, HR, and finance. There are also some public documents. Four users map to those departments:

- `alice` → engineering
- `bob` → sales
- `hr_manager` → HR
- `finance_manager` → finance

Department membership drives most access. An engineering document is visible to all engineering members by default. On top of that, there are three cross-department grants (for example, the engineering architecture document is also visible to Sales) and three individual exceptions. Public documents are granted to all four users explicitly. There is no `public` role in the schema — every permission is a concrete relationship in SpiceDB.

### The agent graph

The agent is a directed graph with four nodes:

```
retrieve → authorize → [reason] → generate
```

**Retrieval** embeds the user's query using OpenAI's `text-embedding-3-small` and searches the Milvus `Documents` collection for the top 5 semantically similar results.

**Authorization** is the security boundary. It batch-checks every retrieved document against SpiceDB and splits them into authorized and denied sets. The graph structure enforces that this step is never skipped.

**Reasoning** is optional. With `max_attempts=1` (the default), if all retrieved documents are denied, the agent goes straight to generation with an explanation. With `max_attempts > 1`, an LLM reasoning step kicks in: it can decide to retry with a modified query strategy. This is where the "agentic" part earns its name — the agent can recognize that its initial retrieval missed the mark and try again.

**Generation** builds the final answer using only the authorized documents as context. The prompt is explicit: use only what's in the documents, quote directly, and if some results were denied, say so.

## Milvus Setup

Create a Milvus collection that includes a `doc_id` field. This field is the link between Milvus and SpiceDB — it maps each retrieved document to the resource ID that SpiceDB checks permissions against.

The demo uses `text-embedding-3-small`, which produces 1536-dimensional vectors. The index is `IVF_FLAT` with `COSINE` metric, which is sufficient for a demo corpus.

```python
from pymilvus import MilvusClient, DataType

client = MilvusClient(uri="http://localhost:19530")

if client.has_collection("Documents"):
    client.drop_collection("Documents")

schema = client.create_schema(auto_id=False, enable_dynamic_field=False)
schema.add_field("doc_id", DataType.VARCHAR, max_length=256, is_primary=True)
schema.add_field("title", DataType.VARCHAR, max_length=512)
schema.add_field("content", DataType.VARCHAR, max_length=65535)
schema.add_field("department", DataType.VARCHAR, max_length=128)
schema.add_field("classification", DataType.VARCHAR, max_length=128)
schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=1536)

index_params = client.prepare_index_params()
index_params.add_index(
    field_name="embedding",
    metric_type="COSINE",
    index_type="IVF_FLAT",
    params={"nlist": 128},
)

client.create_collection("Documents", schema=schema, index_params=index_params)
```

<div class="alert note">
The <code>department</code> and <code>classification</code> fields are not used by the authorization check, but they are useful metadata to return alongside content in the final response.
</div>

## Ingest documents and write permissions

In a ReBAC system, there are always two writes when the state of the system changes. For example, when a user creates a new document, you write the embedding into Milvus and the access relationship into SpiceDB. Keeping these in sync is the whole game — if a relationship changes in SpiceDB, it immediately affects what gets returned at query time.

First, embed and insert the documents:

```python
import openai

oai_client = openai.OpenAI(api_key="sk-...")

rows = []
for doc in documents:
    response = oai_client.embeddings.create(
        model="text-embedding-3-small",
        input=doc["content"],
    )
    rows.append({
        "doc_id": doc["doc_id"],
        "title": doc["title"],
        "content": doc["content"],
        "department": doc["department"],
        "classification": doc["classification"],
        "embedding": response.data[0].embedding,
    })

client.insert("Documents", rows)
```

Then write the access relationships to SpiceDB. The demo has three relationship patterns:

**Department membership** assigns users to departments. For example, user `alice` belongs to the `engineering` org:

```python
from authzed.api.v1 import (
    WriteRelationshipsRequest, RelationshipUpdate,
    Relationship, ObjectReference, SubjectReference,
)

# alice is a member of engineering
RelationshipUpdate(
    operation=RelationshipUpdate.Operation.OPERATION_TOUCH,
    relationship=Relationship(
        resource=ObjectReference(object_type="department", object_id="engineering"),
        relation="member",
        subject=SubjectReference(
            object=ObjectReference(object_type="user", object_id="alice")
        ),
    ),
)
```

**Department-based document access** grants view permission to all members of a department at once, using the `department#member` subject type.

**Individual exceptions** grant access to a specific user regardless of department. The code for all relationship patterns is similar — only the `subjects` and `objects` differ.

Once all relationships are written:

```python
spicedb_client.WriteRelationships(WriteRelationshipsRequest(updates=updates))
```

## Two strategies: pick your tradeoff

There are two fundamental ways to ensure your RAG returns responses based only on what the user is authorized to view.

**Pre-filter** calls SpiceDB's `LookupResources` before touching Milvus. It returns every document the user can see, and you pass those IDs as a filter expression to Milvus. Milvus never processes an unauthorized document.

![Pre-filter strategy: SpiceDB resolves accessible documents before the Milvus vector search]({{images.assets/spicedb-prefilter.png "Pre-filter strategy: SpiceDB resolves accessible documents before the Milvus vector search"}})

**Post-filter** inverts the order. Milvus runs a free vector search and returns the top candidates, then SpiceDB batch-checks which ones the user can actually read. SpiceDB has a bulk permissions API, so this is a single API call regardless of how many documents are being checked.

![Post-filter strategy: Milvus retrieves candidates, SpiceDB batch-verifies permissions]({{images.assets/spicedb-postfilter.png "Post-filter strategy: Milvus retrieves candidates, SpiceDB batch-verifies permissions"}})

If your users have access to a small set of documents, the pre-filter approach is recommended. If they have broad access, post-filter is more efficient.

This demo uses **post-filter**. In production, you would likely also combine a coarse-grained technique (such as pre-filtering by `org` or `role`) with a post-filter step to improve performance.

### Authorization is not optional

Asking an AI agent to decide whether authorization is needed is an anti-pattern and can lead to prompt injection attacks and data breaches. LLMs have no concept of "this document is off-limits" — they use whatever context is in the prompt. If unauthorized documents end up in the context window, the model will use them.

The only reliable approach is structural. In this graph, the authorization node sits between retrieval and generation as a fixed edge. The LLM cannot route around it. The reasoning node can decide what to ask for on a retry, but it never sees unauthorized content.

### What `langchain-spicedb` does

The authorization node uses [`langchain-spicedb`](https://github.com/authzed/langchain-spicedb), which wraps SpiceDB's `CheckBulkPermissions` API into a standard LangChain interface:

```python
from langchain_spicedb.core import SpiceDBAuthorizer

authorizer = SpiceDBAuthorizer(
    spicedb_endpoint="localhost:50051",
    spicedb_token="devtoken",
    resource_type="document",
    subject_type="user",
    permission="view",
    resource_id_key="doc_id",  # the metadata field that maps to SpiceDB resource IDs
)

result = await authorizer.filter_documents(
    documents=retrieved_docs,  # list of LangChain Documents
    subject_id="alice",
)

# result.authorized_documents — what the user can read
# result.denied_resource_ids — what got filtered out
```

`filter_documents` takes the list of `Document` objects from retrieval, extracts the `doc_id` from each document's metadata, calls `CheckBulkPermissions` once, and returns an `AuthorizationResult` split into what passed and what was denied. One gRPC call, regardless of how many documents you're checking.

The `doc_id` field is the link between Milvus and SpiceDB. Every document stored in Milvus has a `doc_id` in its metadata. This is the same ID used as the resource object ID when writing relationships to SpiceDB. Keep them in sync and the authorization check always knows what it's checking.

<div class="alert note">
You can run SpiceDB on <a href="https://authzed.com/products/authzed-cloud">AuthZed Cloud</a> to operate your permissions system at enterprise scale.
</div>

## Try it locally

You'll need Docker, Python 3.11+, and an OpenAI API key.

Start the services:

```shell
docker compose up -d
```

This brings up Milvus (plus its etcd and MinIO dependencies) and SpiceDB. Give Milvus about 30 seconds to initialize.

Configure your `.env`:

```
OPENAI_API_KEY=sk-...
MILVUS_URI=http://localhost:19530
SPICEDB_ENDPOINT=localhost:50051
SPICEDB_TOKEN=devtoken
```

Run the setup script. It writes the SpiceDB schema and relationships, then embeds all documents with `text-embedding-3-small` and inserts them into Milvus:

```shell
python examples/setup_environment.py
```

This takes about 30–60 seconds — one embedding call per document.

Then run a query:

```shell
python examples/basic_example.py
```

Or start the UI:

```shell
python run_ui.py
```

Try the same question as different users. Ask `alice` about engineering architecture and she gets results. Ask `bob` the same thing and most results are denied, because the context backing each answer is different.

## Summary

Access control is fundamental to building trustworthy AI systems. In a RAG system, retrieving the most relevant documents is not the same as retrieving the documents the user is allowed to see.

- The full working demo is available at: https://github.com/authzed/examples/tree/main/agentic-rag-authorization
- If you're using LangChain or LangGraph, check out the official `langchain-spicedb` integration: https://docs.langchain.com/oss/python/integrations/providers/spicedb
- SpiceDB is open source: https://github.com/authzed/spicedb
