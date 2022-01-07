# Load Balancing

A segment is the smallest unit of data that a query node manages. The numbers of segments on query nodes and the sizes of segments might differ. Therefore, the speeds of query nodes also differ. In the worst case, a query node is managing many segments slowly. At the same time, some query nodes are being created, which temporarily have no segments stored, that is, cannot provide query services. Thus, CPU resources are wasted.

Assuming that all query nodes have the same RAM size and number of CPU cores, the query coordinator should adjust the number of segments on each query node, that is, to adjust the RAM that each segment uses, and ensure that the total size of segments on each query node is basically the same. Thus, the CPU resources of all query nodes are used evenly, queries are sped up, overloaded query nodes are avoided.

The query coordinator supports balancing segments on all query nodes manually and automatically.

## Automatic balancing
1. The query coordinator checks the RAM usage of all query nodes at regular intervals. Specify the interval by using `balanceIntervalSeconds` in the `milvus.yaml` file. The default value is `60` which indicates 60 seconds.

2. Either of the following condition that evaluates to true triggers automatic balancing of a query node.
	- RAM usage of the query node> `overloadedMemoryThresholdPercentage`
	- |RAM usage of the query node - RAM usage of any query node| > `memoryUsageMaxDifferencePercentage` 
	
<div class="alert note"> 
  <ul>
  <li> RAM usage = Used RAM/Total RAM</li>
  <li>Default values of <code>overloadedMemoryThresholdPercentage</code> and <code>memoryUsageMaxDifferencePercentage</code> are 90% and 30% respectively. Both can be specified in the <code>milvus.yaml</code> file.</li>
  </ul>
</div>

3. To balance a query node, the query coordinator transfers some segments on the query node to another query node (destination). After balancing, the query node should meet the following requirements.
  - RAM usage of the query node <= overloadedMemoryThresholdPercentage

  - |RAM usage 2 of the query node - RAM usage 2 of the dest. node| <  | RAM usage 1 of the query node - RAM usage 1 of the dest. node|

<div class="alert note">RAM usage 1 and RAM usage 2 indicate RAM usage before and after automatic balancing respectively.</div>

4. To transfer segment 1 from  querynode 1 to querynode 2, the query coordinator loads segment 1 on querynode 2. At this point, both querynode 1 and querynode 2 store segment 1. To ensure correct query results, records are deduplicated based on primary keys and segment IDs.

5. To delete segment 1 on querynode 1 which releases RAM, the query coordinator sends `sealedSegmentChangeInfo` to the query channel as follows.

   ```
   sealedSegmentChangeInfo ｛
     onlineNodeID       2
     onlineSegmentIDs   []｛1｝
     offlineNodeID      1
     offlineSegmentIDs   []｛1｝
   ｝
   ```

6. Querynode 1 receives `sealedSegmentChangeInfo` from the query channel. `offlineNodeID` with a value of `1` indicates that querynode 1 should delete segments. `offlineSegmentIDs` with a value of `[]｛1｝` indicates that segment1 should be deleted. Therefore,  segment 1 on querynode 1 is deleted from RAM.

7. At this point, segment 1 has been transferred from querynode 1 to querynode 2 for load balancing.

## Manual balancing

### Show segment information

Use the `pymilvus.utility.get_query_segment_info()` method to show the information of segments on query nodes.

See [API Reference](https://milvus.io/api-reference/pymilvus/v2.0.0rc8/api/utility.html#pymilvus.utility.get_query_segment_info) for more information about the syntax and parameters.

#### Sample response

```Groovy
[segmentID: 429189132961972225
collectionID: 429189132791516481   // collectionID corresponding to collection_name 
partitionID: 429189132791516482
mem_size: 267395040.  // the memory size of the segment
num_rows: 506430      // the num rows of segment
index_name: "_default_idx"
indexID: 429189147524071425
nodeID: 7             // query node ID
state: Sealed         // segment state including {growing, sealed}
, segmentID: 429189132961972226
collectionID: 429189132791516481
partitionID: 429189132791516482
mem_size: 271164960
num_rows: 513570
index_name: "_default_idx"
indexID: 429189147524071425
nodeID: 7
state: Sealed
]
```
### Transfer segments

Run the following code to transfer the segment with segmentID `429189132961972226`  to a new node with nodeID `8`.

```Python
pymilvus.utility.load_balance(src_node_id=7, dst_node_ids=[8], sealed_segment_ids=[429189132961972226])
```
|Parameter|Required|Description|
|---|---|---|
|`src_node_id`|Yes|The nodeID of the query node to be balanced.|
|`dst_node_ids`|No|The nodeIDs of the query nodes to transfer segments to. If you do not specify this parameter, the system decides the query nodes to transfer segments to automatically. |
|`sealed_segment_ids`|No|The nodeIDs of the segments to be transferred. If you do not specify this parameter, all sealed segments on the query node with nodeID `src_node_id` are transferred to other query nodes. |
