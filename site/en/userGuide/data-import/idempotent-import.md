---
id: idempotent-import.md
title: "Idempotent Bulk Import"
summary: "Send an idempotency key so that a retried bulk import resolves to the original job instead of creating a second one."
---

# Idempotent Bulk Import

A bulk import request can succeed while its response is lost: the call times out, the connection drops, or your orchestrator dies before it saves the returned `jobId`. You cannot tell "not done" from "done, reply lost". Retrying starts a second job and every row lands twice; not retrying may lose the import.

An idempotency key removes the choice. Tag the request with one, and a retry carrying the same key returns the original `jobId` instead of creating a second job.

<!-- TODO: 3.0.2 is the first 3.0 release after the cherry-pick (milvus-io/milvus#53228) and is not tagged yet; confirm the number once it ships. 2.6.24 is tagged and contains milvus-io/milvus#53236. -->
Idempotent bulk import requires Milvus 3.0.2 or later, or 2.6.24 or later on the 2.6 line. An older server ignores the header and every request, retry or not, starts a new job.

## Sending the key

The key travels as the `Idempotency-Key` HTTP header, not in the request body.

```bash
curl -X POST "http://localhost:19530/v2/vectordb/jobs/import/create" \
  -H "Authorization: Bearer root:Milvus" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: nightly-2026-09-07-batch-3" \
  -d '{"collectionName": "events", "files": [["events/part-0.parquet"]]}'
```

<!-- TODO: after milvus-io/pymilvus#3784 is released, verify this example against the released API and name the minimum pymilvus version in the paragraph below. -->
```python
from pymilvus.bulk_writer import IDEMPOTENCY_KEY_HEADER, bulk_import

resp = bulk_import(
    url="http://localhost:19530",
    collection_name="events",
    files=[["events/2026-09-07/part-0.parquet"]],
    headers={IDEMPOTENCY_KEY_HEADER: "nightly-2026-09-07-batch-3"},
)
resp.json()["data"]["jobId"]   # the same id on every retry
```

`IDEMPOTENCY_KEY_HEADER` is `"Idempotency-Key"`; the raw string works too. A pymilvus older than the one that added the `headers` parameter sends no key, and the import behaves as a normal, non-idempotent one.

Poll `/v2/vectordb/jobs/import/describe` with the returned `jobId` as usual. A retry that arrives while the original is still being registered waits for it, so a retry never observes a half-registered job.

## Choosing a key

- **One key per logical request.** Name the unit of work, such as `orders-2026-09-07-batch-3`, or generate a UUID and store it with the work item before you send the request.
- **Retry with the same key.** Minting a new key on a retry is what duplicates data. The exceptions are listed under [When to send a new key](#when-to-send-a-new-key).
- **Never reuse a key for different files.** Milvus does not compare the two requests. You get the original `jobId` back, and the new files are not imported.
- **Keep it short and printable.** Printable ASCII, at most 256 bytes by default (`streaming.idempotency.maxKeyLength`). Anything else is rejected with error `1100`.
- **Do not put secrets in it.** The key is stored with your data.

## How long a key is remembered

The key is scoped to the collection by its internal ID, so renaming the collection does not break a retry, as long as the retry names the collection by its new name. Dropping and recreating the collection under the same name does break it, and a fresh job is the right answer there.

Milvus remembers an import key for about a day. Treat that as nominal rather than guaranteed: heavy DDL or import traffic shortens it, and a coordinator restart lengthens it. A retry after the key is forgotten starts a fresh job.

## When to send a new key

Two cases, and only two:

- **The original job failed.** Retrying the key returns that same failed `jobId` for as long as the key is remembered. Fix the cause, then send a new key.
- **The original job was cleaned up.** Milvus keeps finished jobs for `dataCoord.import.taskRetention` (48 hours by default). If that expires while the key is still remembered, the retry hands back a `jobId` that no longer describes. Send a new key.

## Configuration

Two parameters bound the behavior on this page. Neither needs changing for the key to work.

| Parameter | Default | What it does |
|---|---|---|
| `streaming.walBroadcaster.tombstone.maxLifetime` | `24h` | How long an import key is remembered. Not present in the default `milvus.yaml`; add it explicitly to change it. The same store also rejects duplicate DDL submissions, so do not lower it just to shorten the import window. |
| `dataCoord.import.taskRetention` | `172800` (48 hours) | How long a finished import job stays queryable. Keep it comfortably above `maxLifetime`, so that a remembered key always maps to a job that still exists. |
