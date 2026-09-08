---
id: idempotent-requests.md
title: "Idempotent Requests"
summary: "Send an idempotency key so that a retried insert or bulk import is applied at most once and returns the original result."
---

# Idempotent Requests

A request can succeed while its response is lost: the call times out, the connection drops, or your process dies before it reads the reply. You cannot tell "not done" from "done, reply lost". Retrying does the work twice; not retrying may lose it.

An idempotency key removes the choice. Tag a request with one, and a retry carrying the same key returns the original request's result instead of doing the work again.

## Sending the key

The key travels as transport metadata, not in the request body.

```python
from pymilvus import MilvusClient

client = MilvusClient("http://localhost:19530")
client.insert("events", rows, idempotency_key="order-4711")
```

```go
client.Insert(ctx, milvusclient.NewColumnBasedInsertOption("events", cols...).
    WithIdempotencyKey("order-4711"))
```

```bash
curl -X POST "http://localhost:19530/v2/vectordb/jobs/import/create" \
  -H "Authorization: Bearer root:Milvus" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: nightly-2026-09-07-batch-3" \
  -d '{"collectionName": "events", "files": [["events/part-0.parquet"]]}'
```

Over REST the header is `Idempotency-Key`. Over gRPC it is the `idempotency-key` metadata entry. SDK support is pending release; this page will name the minimum versions once they ship.

<div class="alert note">

Two operations honor the key today: **insert** and **bulk import**. Any other endpoint accepts a well-formed key and ignores it, except the Go SDK's `Upsert`, which rejects one outright.

</div>

## Choosing a key

- **One key per logical request.** Name the unit of work, such as `orders-2026-09-07-batch-3`, or generate a UUID and store it with the work item before you send the request.
- **Retry with the same key.** Minting a new key on a retry is what duplicates data. The exceptions are listed under each operation below.
- **Never reuse a key for different data.** Milvus does not compare the two requests. You get the original result back, and the new data may be partly written or not written at all.
- **Keep it short and printable.** At most 256 bytes of printable ASCII. Anything else is rejected with error `1100`.
- **Do not put secrets in it.** The key is stored with your data.

## Insert

Retrying an insert normally writes the rows twice, and under `autoID` you cannot even find the duplicates by primary key, because the retry gets new IDs. With a key, the retry writes nothing and returns the original result, the original IDs included.

### Turn it on

Idempotent insert is off by default and needs both a cluster setting and a collection property:

```yaml
streaming:
  idempotency:
    enabled: true
```

```python
client.alter_collection_properties(
    "events", properties={"collection.insert.idempotency.enabled": "true"}
)
```

Sending a key before both are on fails with error `1100`.

### What a retry looks like

```python
rows = [{"order_id": 4711, "vector": [0.1, 0.2, 0.3]}]

res = client.insert("events", rows, idempotency_key="order-4711")
# {"insert_count": 1, "ids": [<auto-id>]}

# ... the response is lost, so the client retries ...

res = client.insert("events", rows, idempotency_key="order-4711")
# {"insert_count": 1, "ids": [<auto-id>]}   same id, no second row
```

A retry that arrives while the original is still being written waits for it, then returns its result. If the original failed, nothing landed and the retry writes normally.

### Keys you did not send

With idempotent insert on, an insert without a key still gets one, derived from the collection, partition and row data. A byte-identical retry therefore deduplicates on its own.

<div class="alert note">

The derived key cannot tell a retry apart from a second, intentional insert of identical rows. If your workload writes the same payload more than once on purpose, give each write its own explicit key, or leave the collection property off.

</div>

### How far back it remembers

Each shard remembers recent keys up to a byte budget, backed by a durable copy that survives a restart. There is no time limit, so an outage alone does not forget your key. Other writes do: the budget is shared, so heavy traffic on the same shard, or on collections that share its channel, can evict a key while you are down. A retry after that is a fresh insert.

Dropping or truncating the collection, or dropping a partition, forgets the keys for the affected shard.

## Bulk import

An import returns a `jobId`. If your orchestrator crashes after Milvus accepted the import but before it saved that ID, the retry starts a second job and every row lands twice. With a key, the retry returns the original `jobId`.

```python
from pymilvus.bulk_writer import bulk_import

resp = bulk_import(
    url="http://localhost:19530",
    collection_name="events",
    files=[["events/2026-09-07/part-0.parquet"]],
    idempotency_key="nightly-2026-09-07-batch-3",
)
# {"jobId": "<job-id>"}   the same id on every retry
```

Poll `/v2/vectordb/jobs/import/describe` with that `jobId` as usual. A retry that arrives mid-registration waits, so the ID you get back always belongs to a job that was created.

The key is scoped to the collection by its internal ID, so renaming the collection does not break a retry. Dropping and recreating it under the same name does, and a fresh job is the right answer there.

Milvus remembers an import key for about a day. Treat that as nominal rather than guaranteed: heavy DDL or import traffic shortens it, and a coordinator restart lengthens it.

### When to send a new key

Two cases, and only two:

- **The original job failed.** Retrying the key returns that same failed `jobId` forever. Fix the cause, then send a new key.
- **The original job was cleaned up.** Milvus keeps finished jobs for `dataCoord.import.taskRetention` (48 hours by default). If that expires while the key is still remembered, the retry hands back a `jobId` that no longer describes. Send a new key.

Keep `taskRetention` comfortably above the key window so the second case stays rare.

## Configuration

The feature is controlled by `streaming.idempotency.enabled` plus the per-collection property, and its limits by the other `streaming.idempotency.*` parameters. None of them appear in the default `milvus.yaml`; add a key explicitly to change it. See the system configuration reference for the full list and defaults.
