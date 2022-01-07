# Milvus Compaction Principle
This topic describes the principle of Milvus compaction.
## What is compaction?

Databases like LevelDB and RocksDB append data to SSTables. As SSTables increase, the average disk reads per query also increase, which causes inefficient queries. To reduce read amplification and release hard drive space, these databases compact SSTables into one. Compaction processes run in the background automatically. To meet the same requirements, Milvus also supports compaction. With compaction, the following problems are solved.

Similarly, Milvus append inserted and deleted data to binlogs. As binlogs increase, more hard disk space is used. To release hard disk space used by deleted data, Milvus compact binlogs into one.

Additionally, inserted data might form small segments because of auto-flush or user-invoked flush. A segment with less than 1,024 rows will not be indexed and only supports brute-force search to process queries, which causes low query efficiency. To avoid this, Milvus compacts small segments into bigger ones in the background and generates indexes for them to improve query efficiency.


## Configuration

The following table introduces the parameters to configure Milvus compaction.


|Parameter|Description|
|:---|:---|
|`dataCoord.enableCompaction`|Specifies whether to enable compaction. The default value is `false`.|
|`dataCoord.compaction.retentionDuration`|Specifies a period when compaction does not run. The unit is the second. See [Search with Time Travel](https://milvus.io/docs/timetravel.md) for more information.|

Users can trigger a global compaction process manually by calling the `collection.compact()` method. Caution is advised because this operation might take a long time. 

After calling the method, a compaction ID is returned. Users can view the status of the compaction by calling the `collection.get_compaction_state()` method.

Compaction is disabled in Milvus by default. After compaction is enabled, it runs in the background automatically. Additionally, users can invoke compaction manually by using APIs. This process might take a long time. To save time, compaction requests are processed asynchronously.

## Implementation

The following scenarios describe when insert binlogs are generated.

- As inserted data is being appended, the segment reaches the upper limit of size and is automatically flushed to the disk.
- DataCoord automatically flushes segments that stay unsealed for a long time.
- Some APIs automatically invoke flush to write segments to disk.
  

Additionally, when data is deleted, delta binlogs are generated. 

<div class="alert note">Data from a segment is persisted in multiple binlogs. </div>

As mentioned in [What is compaction](#what-is-compaction), compaction includes binlog compaction and segment compaction.

### Binlog compaction

To ensure accurate results of searches with Time Travel, Milvus retains data operated in a period specified by `dataCoord.compaction.retentionDuration`. 

#### Scenarios

- A segment flushes to disk. Compaction runs when either of the following trigger conditions is met.
- Milvus requests global compaction when compaction has not run for a long time. Compaction runs when either of the following trigger conditions is met.
- Users invoke binlog compaction manually. In this case, compaction runs despite delta binlog size and row number. That is, no trigger conditions are required to be met.

#### Trigger conditions

- Rows in delta binlogs are more than 20% of total rows.
- The size of delta binlogs exceeds 10 MB.
  
#### Plan generation

Compact all delta binlogs and insert binlogs that are not retained.

### Segment compaction

To ensure accurate results of searches with Time Travel, Milvus retains data operated in a period specified by `dataCoord.compaction.retentionDuration`. That is, data operated in this period will not be compacted. A segment to compact to cannot exceed the upper limit of size. The default is 512 MB.

#### Scenarios

- A segment flushes to disk.
- Milvus invokes global compaction when compaction does not run for a long time.
- Users invoke segment compaction manually. In this case, compaction runs as long as segments can be compacted into bigger ones. That is, the following  trigger condition is not required to be met.

#### Trigger conditions

Segments smaller than 0.5 * `MaxSegmentSize` is more than 10.

#### Plan generation
Compact smallest segments into bigger ones.

## Notes

Currently, not all parameters to configure compaction are in the `milvus.yaml` file, and plan generation strategies are relatively basic. Everyone is welcome to contribute.