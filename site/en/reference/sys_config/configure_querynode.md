---
id: configure_querynode.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure queryNode for Milvus.
---

# queryNode-related Configurations

Related configuration of queryNode, used to run hybrid search between vector and scalar data.

## `queryNode.stats.publishInterval`

<table id="queryNode.stats.publishInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Interval for querynode to report node information (milliseconds)</li>      </td>
      <td>1000</td>
    </tr>
  </tbody>
</table>


## `queryNode.segcore.knowhereThreadPoolNumRatio`

<table id="queryNode.segcore.knowhereThreadPoolNumRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The number of threads in knowhere's thread pool. If disk is enabled, the pool size will multiply with knowhereThreadPoolNumRatio([1, 32]).</li>      </td>
      <td>4</td>
    </tr>
  </tbody>
</table>


## `queryNode.segcore.knowhereScoreConsistency`

<table id="queryNode.segcore.knowhereScoreConsistency">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>used for zilliz-cloud ; please ignore it for open source.</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `queryNode.segcore.chunkRows`

<table id="queryNode.segcore.chunkRows">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The number of vectors in a chunk.</li>      </td>
      <td>128</td>
    </tr>
  </tbody>
</table>


## `queryNode.segcore.interimIndex.enableIndex`

<table id="queryNode.segcore.interimIndex.enableIndex">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Enable segment build with index to accelerate vector search when segment is in growing or binlog.</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `queryNode.segcore.interimIndex.nlist`

<table id="queryNode.segcore.interimIndex.nlist">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>temp index nlist, recommend to set sqrt(chunkRows), must smaller than chunkRows/8</li>      </td>
      <td>128</td>
    </tr>
  </tbody>
</table>


## `queryNode.segcore.interimIndex.nprobe`

<table id="queryNode.segcore.interimIndex.nprobe">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>nprobe to search small index, based on your accuracy requirement, must smaller than nlist</li>      </td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## `queryNode.segcore.interimIndex.memExpansionRate`

<table id="queryNode.segcore.interimIndex.memExpansionRate">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>extra memory needed by building interim index</li>      </td>
      <td>1.15</td>
    </tr>
  </tbody>
</table>


## `queryNode.segcore.interimIndex.buildParallelRate`

<table id="queryNode.segcore.interimIndex.buildParallelRate">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the ratio of building interim index parallel matched with cpu num</li>      </td>
      <td>0.5</td>
    </tr>
  </tbody>
</table>


## `queryNode.loadMemoryUsageFactor`

<table id="queryNode.loadMemoryUsageFactor">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The multiply factor of calculating the memory usage while loading segments</li>      </td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## `queryNode.enableDisk`

<table id="queryNode.enableDisk">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>enable querynode load disk index, and search on disk index</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `queryNode.maxDiskUsagePercentage`

<table id="queryNode.maxDiskUsagePercentage">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>95</td>
    </tr>
  </tbody>
</table>


## `queryNode.cache.enabled`

<table id="queryNode.cache.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `queryNode.cache.memoryLimit`

<table id="queryNode.cache.memoryLimit">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>2 GB, 2 * 1024 *1024 *1024</li>      </td>
      <td>2147483648</td>
    </tr>
  </tbody>
</table>


## `queryNode.cache.readAheadPolicy`

<table id="queryNode.cache.readAheadPolicy">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The read ahead policy of chunk cache, options: `normal, random, sequential, willneed, dontneed`</li>      </td>
      <td>willneed</td>
    </tr>
  </tbody>
</table>


## `queryNode.cache.warmup`

<table id="queryNode.cache.warmup">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>options: async, sync, off. </li>
        <li>Specifies the necessity for warming up the chunk cache. </li>
        <li>1. If set to "sync" or "async," the original vector data will be synchronously/asynchronously loaded into the </li>
        <li>chunk cache during the load process. This approach has the potential to substantially reduce query/search latency</li>
        <li>for a specific duration post-load, albeit accompanied by a concurrent increase in disk usage;</li>
        <li>2. If set to "off," original vector data will only be loaded into the chunk cache during search/query.</li>      </td>
      <td>async</td>
    </tr>
  </tbody>
</table>


## `queryNode.mmap.mmapEnabled`

<table id="queryNode.mmap.mmapEnabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Enable mmap for loading data</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `queryNode.lazyload.enabled`

<table id="queryNode.lazyload.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Enable lazyload for loading data</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `queryNode.lazyload.waitTimeout`

<table id="queryNode.lazyload.waitTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>max wait timeout duration in milliseconds before start to do lazyload search and retrieve</li>      </td>
      <td>30000</td>
    </tr>
  </tbody>
</table>


## `queryNode.lazyload.requestResourceTimeout`

<table id="queryNode.lazyload.requestResourceTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>max timeout in milliseconds for waiting request resource for lazy load, 5s by default</li>      </td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## `queryNode.lazyload.requestResourceRetryInterval`

<table id="queryNode.lazyload.requestResourceRetryInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>retry interval in milliseconds for waiting request resource for lazy load, 2s by default</li>      </td>
      <td>2000</td>
    </tr>
  </tbody>
</table>


## `queryNode.lazyload.maxRetryTimes`

<table id="queryNode.lazyload.maxRetryTimes">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>max retry times for lazy load, 1 by default</li>      </td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## `queryNode.lazyload.maxEvictPerRetry`

<table id="queryNode.lazyload.maxEvictPerRetry">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>max evict count for lazy load, 1 by default</li>      </td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## `queryNode.grouping.enabled`

<table id="queryNode.grouping.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `queryNode.grouping.maxNQ`

<table id="queryNode.grouping.maxNQ">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>1000</td>
    </tr>
  </tbody>
</table>


## `queryNode.grouping.topKMergeRatio`

<table id="queryNode.grouping.topKMergeRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>20</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.receiveChanSize`

<table id="queryNode.scheduler.receiveChanSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>10240</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.unsolvedQueueSize`

<table id="queryNode.scheduler.unsolvedQueueSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>10240</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.maxReadConcurrentRatio`

<table id="queryNode.scheduler.maxReadConcurrentRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>maxReadConcurrentRatio is the concurrency ratio of read task (search task and query task).</li>
        <li>Max read concurrency would be the value of hardware.GetCPUNum * maxReadConcurrentRatio.</li>
        <li>It defaults to 2.0, which means max read concurrency would be the value of hardware.GetCPUNum * 2.</li>
        <li>Max read concurrency must greater than or equal to 1, and less than or equal to hardware.GetCPUNum * 100.</li>
        <li>(0, 100]</li>      </td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.cpuRatio`

<table id="queryNode.scheduler.cpuRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>ratio used to estimate read task cpu usage.</li>      </td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.maxTimestampLag`

<table id="queryNode.scheduler.maxTimestampLag">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>86400</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.scheduleReadPolicy.name`

<table id="queryNode.scheduler.scheduleReadPolicy.name">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>fifo: A FIFO queue support the schedule.</li>
        <li>user-task-polling:</li>
        <li>	The user's tasks will be polled one by one and scheduled.</li>
        <li>	Scheduling is fair on task granularity.</li>
        <li>	The policy is based on the username for authentication.</li>
        <li>	And an empty username is considered the same user.</li>
        <li>	When there are no multi-users, the policy decay into FIFO"</li>      </td>
      <td>fifo</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.scheduleReadPolicy.taskQueueExpire`

<table id="queryNode.scheduler.scheduleReadPolicy.taskQueueExpire">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Control how long (many seconds) that queue retains since queue is empty</li>      </td>
      <td>60</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.scheduleReadPolicy.enableCrossUserGrouping`

<table id="queryNode.scheduler.scheduleReadPolicy.enableCrossUserGrouping">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Enable Cross user grouping when using user-task-polling policy. (Disable it if user's task can not merge each other)</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `queryNode.scheduler.scheduleReadPolicy.maxPendingTaskPerUser`

<table id="queryNode.scheduler.scheduleReadPolicy.maxPendingTaskPerUser">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Max pending task per user in scheduler</li>      </td>
      <td>1024</td>
    </tr>
  </tbody>
</table>


## `queryNode.dataSync.flowGraph.maxQueueLength`

<table id="queryNode.dataSync.flowGraph.maxQueueLength">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum length of task queue in flowgraph</li>      </td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## `queryNode.dataSync.flowGraph.maxParallelism`

<table id="queryNode.dataSync.flowGraph.maxParallelism">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum number of tasks executed in parallel in the flowgraph</li>      </td>
      <td>1024</td>
    </tr>
  </tbody>
</table>


## `queryNode.enableSegmentPrune`

<table id="queryNode.enableSegmentPrune">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>use partition prune function on shard delegator</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `queryNode.ip`

<table id="queryNode.ip">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>if not specified, use the first unicastable address</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `queryNode.port`

<table id="queryNode.port">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>21123</td>
    </tr>
  </tbody>
</table>


## `queryNode.grpc.serverMaxSendSize`

<table id="queryNode.grpc.serverMaxSendSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>536870912</td>
    </tr>
  </tbody>
</table>


## `queryNode.grpc.serverMaxRecvSize`

<table id="queryNode.grpc.serverMaxRecvSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>268435456</td>
    </tr>
  </tbody>
</table>


## `queryNode.grpc.clientMaxSendSize`

<table id="queryNode.grpc.clientMaxSendSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>268435456</td>
    </tr>
  </tbody>
</table>


## `queryNode.grpc.clientMaxRecvSize`

<table id="queryNode.grpc.clientMaxRecvSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>536870912</td>
    </tr>
  </tbody>
</table>


