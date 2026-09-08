---
id: idempotent-requests.md
title: "Idempotent Requests"
summary: "Send an idempotency key so that a retried insert or bulk import is applied at most once and returns the original result."
---

# Idempotent Requests

Milvus can deduplicate a retried request when the client tags it with an idempotency key. A retry that carries the same key as an earlier request returns the earlier request's result instead of doing the work again.

<div class="alert note">

Sending an idempotency key requires a client that supports it: pymilvus with the `idempotency_key` argument, or a Go SDK with `WithIdempotencyKey`. An older client silently sends no key, and the request behaves as a normal, non-idempotent one.

</div>

## Why you need it

A request can succeed while its response is lost: the client times out, the connection drops, or the client crashes before it saves the response. The client cannot tell "not done" from "done, response lost". Without an idempotency key, retrying does the work a **second time** and not retrying may lose it. With an idempotency key the retry resolves to the **original** request and returns its result.

## Sending the key

Attach the key to the request as transport metadata. It is not part of the request body.

| Transport | Where to put it  | Name              |
|-----------|------------------|-------------------|
| REST      | HTTP header      | `Idempotency-Key` |
| gRPC      | Request metadata | `idempotency-key` |

Milvus reads the key the same way on both transports. On a collection where idempotency is off, a request without a key behaves exactly as before. On a collection with idempotent insert enabled, a keyless insert is deduplicated by its own content, as described under Explicit and automatic keys.

### pymilvus

```python
from pymilvus import MilvusClient

client = MilvusClient("http://localhost:19530")
client.insert("events", rows, idempotency_key="order-4711")
```

### Go SDK

```go
client.Insert(ctx, milvusclient.NewColumnBasedInsertOption("events", cols...).
    WithIdempotencyKey("order-4711"))
```

### REST

```bash
curl -X POST "http://localhost:19530/v2/vectordb/<endpoint>" \
  -H "Authorization: Bearer root:Milvus" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: <your-key>" \
  -d '<request body>'
```

## Supported operations

| Operation   | Entry point | Key scope |
|-------------|-------------|-----------|
| Insert      | `client.insert(..., idempotency_key=...)` | Shard |
| Bulk import | `POST /v2/vectordb/jobs/import/create`, `bulk_import(idempotency_key=...)` | Collection |

An operation not in this table carries no idempotency guarantee. Over REST and in pymilvus it accepts a well-formed key and ignores it. The Go SDK is stricter: passing a key to `Upsert` returns a parameter error before the request is sent.

## Rules that hold everywhere

- **One key per logical request.** A good key names the unit of work, such as `<pipeline>-<date>-<batch>`, or a UUID you store next to the work item before you send the request.
- **Never reuse a key for a different request.** Milvus does not compare the retry's body against the original. A reused key returns the old result and silently skips the new work.
- **Retry with the same key.** A rejected retry is not a reason to mint a new key. The exceptions are listed per operation below.
- **At most 256 bytes, printable ASCII only.** Milvus rejects anything else on every endpoint with error code `1100` (invalid parameter). The bound is `streaming.idempotency.maxKeyLength`.
- **Do not put secrets in the key.** Milvus stores it verbatim in the write-ahead log and in metadata.

## Insert

An insert that times out or loses its response leaves the client unable to tell whether the rows landed. Retrying may write them twice; under autoID the duplicates are not even detectable by primary key, because a retry gets new IDs. With an idempotency key the retry is applied at most once and returns the original result, including the original primary keys.

### Enabling it

Idempotent insert is off by default. Turn on the global switch and the collection property:

```yaml
streaming:
  idempotency:
    enabled: true
```

```python
client.create_collection(
    "events",
    schema=schema,
    properties={"collection.insert.idempotency.enabled": "true"},
)
# or on an existing collection
client.alter_collection_properties(
    "events", properties={"collection.insert.idempotency.enabled": "true"}
)
```

An insert that carries a key while either switch is off is rejected with error code `1100`.

### What happens on a retry

```python
rows = [{"order_id": 4711, "vector": [0.1, 0.2, 0.3]}]

res = client.insert("events", rows, idempotency_key="order-4711")
# res == {"insert_count": 1, "ids": [<auto-id>]}
```

1. The client sends the insert with key `order-4711`. Milvus writes the row, assigns autoID `<auto-id>`, and returns it.
2. The response is lost: the call times out, or the process dies before it reads the result.
3. The client sends the same insert with the same key.
4. Milvus recognizes the key, writes nothing, and returns the original result, with the same `ids`.

```python
res = client.insert("events", rows, idempotency_key="order-4711")
# res == {"insert_count": 1, "ids": [<auto-id>]}   same <auto-id>, no second row
```

The collection holds the row once. A client that stores the returned IDs sees stable values across retries.

### Explicit and automatic keys

Send a key the same way as for any other operation. If you send none, Milvus derives one from the request itself: the database, collection, partition, and the row data as the client sent them. A byte-identical retry therefore deduplicates on its own, with no client change. Field order does not matter, because Milvus sorts fields before hashing them; row order and encoding do. Send an explicit key when your retry may differ in those, or when you want to control the key yourself.

<div class="alert note">

**Two distinct inserts with the same payload are treated as one.** The automatic key is a hash of the content, so it cannot tell a retry apart from a second, intentional insert of identical rows. On a collection with idempotent insert enabled, the second one returns the first one's result, including its primary keys, and writes nothing. No error is raised. If your workload legitimately inserts identical payloads more than once, give each insert its own explicit key, or leave the collection property off.

</div>

### Scope and window

The key deduplicates per **shard**. A single insert fans out to one write per shard, and each shard keeps its own record. On a retry, shards that already hold the key return the original result and shards that never received it apply the write. That is the intended behavior after a partial failure.

The window is measured in **bytes of writes, not in time**. Each shard keeps up to `streaming.idempotency.maxBytesPerWindow` of recent insert records in memory, backed by a durable copy that survives a restart or a failover. On a busy shard the window may span minutes; on a quiet one it may span days. There is no time limit, so an outage does not empty the window, which is exactly when a resuming client needs it. Turning the feature off does empty it, as described below.

### Cases to know

**The collection was emptied.** `DropCollection`, `TruncateCollection`, and `DropPartition` clear the affected shard's records. A retry after one of them is a fresh write, which is correct, since the rows it would have deduplicated against are gone. `DropPartition` clears the whole shard, not only the dropped partition.

**The original insert failed.** In the usual case nothing landed, the key was released, and a retry with the same key writes normally. One exception: some message queues can persist a write while still reporting an error, so a retry after such a failure can write the rows a second time. That is the same outcome a retry without an idempotency key would produce.

**The global switch was turned off.** Turning off `streaming.idempotency.enabled` and restarting discards every stored insert record on every shard. Re-enabling starts from an empty window, so a retry of an insert sent before the toggle is written as a fresh insert.

**The key was reused with a different payload.** Milvus returns the original result. If the retry's primary key shape does not match the original, the insert fails with "idempotency key was reused with a different payload". Either way, the new rows are not written.

**Renames and automatic keys.** An automatic key is derived from names, so a retry after a rename derives a different key and is written as a fresh insert. An explicit key is unaffected.

## Bulk import

An import request returns a `jobId`. If an orchestrator (Airflow, Temporal, a cron job, a shell script) crashes after Milvus accepted the import but before it saved that `jobId`, the orchestrator retries. Without a key the retry starts a **second job** that imports the same files again, and the collection ends up with every row twice.

### What happens on a retry

```python
from pymilvus.bulk_writer import bulk_import

resp = bulk_import(
    url="http://localhost:19530",
    collection_name="events",
    files=[["events/2026-09-07/part-0.parquet"]],
    idempotency_key="nightly-2026-09-07-batch-3",
)
# resp.json()["data"]["jobId"] == "<job-id>"
```

1. The orchestrator sends the import with key `nightly-2026-09-07-batch-3`. Milvus creates job `<job-id>` and returns it.
2. The orchestrator crashes before it records the `jobId`.
3. The orchestrator restarts and sends the same request with the same key.
4. Milvus recognizes the key, creates no new job, and returns `<job-id>` again.
5. The orchestrator polls `/v2/vectordb/jobs/import/describe` with that `jobId` as usual.

The collection receives the rows exactly once. A retry that arrives while the original job is still being registered waits for that registration to finish, so the returned `jobId` always refers to a job that exists.

### Scope and window

The key deduplicates within one collection, identified by its internal ID, not its name. Renaming the collection between the request and the retry does not break the match, as long as the retry uses the current name. Dropping the collection and recreating one with the same name does break it, because the retry now targets a different collection, and a fresh job is the correct outcome.

Milvus remembers an import key for up to 24 hours by default. A cluster with heavy DDL or import traffic can forget keys sooner, because the record store is also capped by count. A retry after the window starts a new job.

### Cases to know

**The original job failed.** A retry with the same key returns the same failed `jobId` for the rest of the window. Fix the cause and send a new key. This is the one import case where a new key is correct.

**The original job was already cleaned up.** Milvus keeps finished jobs for `dataCoord.import.taskRetention` seconds. If a retry lands inside the idempotency window but after the job was removed, you get the original `jobId` back, and the describe call reports that the job does not exist. The default retention covers up to one StreamingCoord restart per tombstone lifetime. Raise `dataCoord.import.taskRetention` if StreamingCoord restarts more often than that.

## Configuration

| Parameter | Default | Effect |
|-----------|---------|--------|
| `streaming.idempotency.maxKeyLength` | 256 | Maximum key length in bytes. Lowering it mid-window rejects retries whose key is longer than the new limit. `0` rejects every key on REST and on any request that reaches a coordinator, but the proxy insert path reads it as unbounded, so do not use `0` to disable the feature. Use `streaming.idempotency.enabled` for that. |
| `streaming.idempotency.enabled` | `false` | Global switch for idempotent insert. Bulk import does not depend on it. Turning it off and restarting discards every stored insert record on every shard; re-enabling starts from an empty window. |
| `streaming.idempotency.maxBytesPerWindow` | 16 MiB | Per-shard in-memory insert record cap. Oldest records are evicted once it is full. |
| `streaming.idempotency.maxRetainedBytes` | 256 MiB | Per-physical-channel budget for the durable insert records. `0` disables the bound. |
| `streaming.idempotency.maxRetainedChunks` | 256 | Per-physical-channel cap on durable record files. When it binds, the insert window is shorter than the byte budget allows. |
| `streaming.walBroadcaster.tombstone.maxLifetime` | 24h | Upper bound of the bulk import window. |
| `streaming.walBroadcaster.tombstone.maxCount` | 8192 | Record cap for the bulk import window. When exceeded, the oldest keys are forgotten before `maxLifetime`. |
| `dataCoord.import.taskRetention` | 172800 (48h) | How long finished import jobs stay queryable. Keep it at least twice `maxLifetime` while clients send keys, because a coordinator restart can extend a key's life by up to another `maxLifetime`. |

Clusters whose clients never send an idempotency key can lower `taskRetention` freely. Its previous default was 10800 (3h).
