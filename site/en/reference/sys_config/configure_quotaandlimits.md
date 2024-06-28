---
id: configure_quotaandlimits.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure quotaAndLimits for Milvus.
---

# quotaAndLimits-related Configurations

QuotaConfig, configurations of Milvus quota and limits.

By default, we enable:

  1. TT protection;

  2. Memory protection.

  3. Disk quota protection.

You can enable:

  1. DML throughput limitation;

  2. DDL, DQL qps/rps limitation;

  3. DQL Queue length/latency protection;

  4. DQL result rate protection;

If necessary, you can also manually force to deny RW requests.

## `quotaAndLimits.enabled`

<table id="quotaAndLimits.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>`true` to enable quota and limits, `false` to disable.</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.quotaCenterCollectInterval`

<table id="quotaAndLimits.quotaCenterCollectInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>quotaCenterCollectInterval is the time interval that quotaCenter</li>
        <li>collects metrics from Proxies, Query cluster and Data cluster.</li>
        <li>seconds, (0 ~ 65536)</li>      </td>
      <td>3</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.ddl.enabled`

<table id="quotaAndLimits.ddl.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.ddl.collectionRate`

<table id="quotaAndLimits.ddl.collectionRate">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit, rate for CreateCollection, DropCollection, LoadCollection, ReleaseCollection</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.ddl.partitionRate`

<table id="quotaAndLimits.ddl.partitionRate">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit, rate for CreatePartition, DropPartition, LoadPartition, ReleasePartition</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.ddl.db.collectionRate`

<table id="quotaAndLimits.ddl.db.collectionRate">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps of db level , default no limit, rate for CreateCollection, DropCollection, LoadCollection, ReleaseCollection</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.ddl.db.partitionRate`

<table id="quotaAndLimits.ddl.db.partitionRate">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps of db level, default no limit, rate for CreatePartition, DropPartition, LoadPartition, ReleasePartition</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.indexRate.enabled`

<table id="quotaAndLimits.indexRate.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.indexRate.max`

<table id="quotaAndLimits.indexRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit, rate for CreateIndex, DropIndex</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.indexRate.db.max`

<table id="quotaAndLimits.indexRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps of db level, default no limit, rate for CreateIndex, DropIndex</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.flushRate.enabled`

<table id="quotaAndLimits.flushRate.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.flushRate.max`

<table id="quotaAndLimits.flushRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit, rate for flush</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.flushRate.collection.max`

<table id="quotaAndLimits.flushRate.collection.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit, rate for flush at collection level.</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.flushRate.db.max`

<table id="quotaAndLimits.flushRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps of db level, default no limit, rate for flush</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.compactionRate.enabled`

<table id="quotaAndLimits.compactionRate.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.compactionRate.max`

<table id="quotaAndLimits.compactionRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit, rate for manualCompaction</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.compactionRate.db.max`

<table id="quotaAndLimits.compactionRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps of db level, default no limit, rate for manualCompaction</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.enabled`

<table id="quotaAndLimits.dml.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>dml limit rates, default no limit.</li>
        <li>The maximum rate will not be greater than max.</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.insertRate.max`

<table id="quotaAndLimits.dml.insertRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.insertRate.db.max`

<table id="quotaAndLimits.dml.insertRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.insertRate.collection.max`

<table id="quotaAndLimits.dml.insertRate.collection.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.insertRate.partition.max`

<table id="quotaAndLimits.dml.insertRate.partition.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.upsertRate.max`

<table id="quotaAndLimits.dml.upsertRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.upsertRate.db.max`

<table id="quotaAndLimits.dml.upsertRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.upsertRate.collection.max`

<table id="quotaAndLimits.dml.upsertRate.collection.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.upsertRate.partition.max`

<table id="quotaAndLimits.dml.upsertRate.partition.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.deleteRate.max`

<table id="quotaAndLimits.dml.deleteRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.deleteRate.db.max`

<table id="quotaAndLimits.dml.deleteRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.deleteRate.collection.max`

<table id="quotaAndLimits.dml.deleteRate.collection.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.deleteRate.partition.max`

<table id="quotaAndLimits.dml.deleteRate.partition.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.bulkLoadRate.max`

<table id="quotaAndLimits.dml.bulkLoadRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit, not support yet. TODO: limit bulkLoad rate</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.bulkLoadRate.db.max`

<table id="quotaAndLimits.dml.bulkLoadRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit, not support yet. TODO: limit db bulkLoad rate</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.bulkLoadRate.collection.max`

<table id="quotaAndLimits.dml.bulkLoadRate.collection.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit, not support yet. TODO: limit collection bulkLoad rate</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dml.bulkLoadRate.partition.max`

<table id="quotaAndLimits.dml.bulkLoadRate.partition.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB/s, default no limit, not support yet. TODO: limit partition bulkLoad rate</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.enabled`

<table id="quotaAndLimits.dql.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>dql limit rates, default no limit.</li>
        <li>The maximum rate will not be greater than max.</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.searchRate.max`

<table id="quotaAndLimits.dql.searchRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>vps (vectors per second), default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.searchRate.db.max`

<table id="quotaAndLimits.dql.searchRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>vps (vectors per second), default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.searchRate.collection.max`

<table id="quotaAndLimits.dql.searchRate.collection.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>vps (vectors per second), default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.searchRate.partition.max`

<table id="quotaAndLimits.dql.searchRate.partition.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>vps (vectors per second), default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.queryRate.max`

<table id="quotaAndLimits.dql.queryRate.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.queryRate.db.max`

<table id="quotaAndLimits.dql.queryRate.db.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.queryRate.collection.max`

<table id="quotaAndLimits.dql.queryRate.collection.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.dql.queryRate.partition.max`

<table id="quotaAndLimits.dql.queryRate.partition.max">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>qps, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limits.maxCollectionNum`

<table id="quotaAndLimits.limits.maxCollectionNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>65536</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limits.maxCollectionNumPerDB`

<table id="quotaAndLimits.limits.maxCollectionNumPerDB">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>65536</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limits.maxInsertSize`

<table id="quotaAndLimits.limits.maxInsertSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>maximum size of a single insert request, in bytes, -1 means no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limits.maxResourceGroupNumOfQueryNode`

<table id="quotaAndLimits.limits.maxResourceGroupNumOfQueryNode">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>maximum number of resource groups of query nodes</li>      </td>
      <td>1024</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.forceDeny`

<table id="quotaAndLimits.limitWriting.forceDeny">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>forceDeny false means dml requests are allowed (except for some</li>
        <li>specific conditions, such as memory of nodes to water marker), true means always reject all dml requests.</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.ttProtection.enabled`

<table id="quotaAndLimits.limitWriting.ttProtection.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.ttProtection.maxTimeTickDelay`

<table id="quotaAndLimits.limitWriting.ttProtection.maxTimeTickDelay">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>maxTimeTickDelay indicates the backpressure for DML Operations.</li>
        <li>DML rates would be reduced according to the ratio of time tick delay to maxTimeTickDelay,</li>
        <li>if time tick delay is greater than maxTimeTickDelay, all DML requests would be rejected.</li>
        <li>seconds</li>      </td>
      <td>300</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.memProtection.enabled`

<table id="quotaAndLimits.limitWriting.memProtection.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>When memory usage > memoryHighWaterLevel, all dml requests would be rejected;</li>
        <li>When memoryLowWaterLevel < memory usage < memoryHighWaterLevel, reduce the dml rate;</li>
        <li>When memory usage < memoryLowWaterLevel, no action.</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.memProtection.dataNodeMemoryLowWaterLevel`

<table id="quotaAndLimits.limitWriting.memProtection.dataNodeMemoryLowWaterLevel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>(0, 1], memoryLowWaterLevel in DataNodes</li>      </td>
      <td>0.85</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.memProtection.dataNodeMemoryHighWaterLevel`

<table id="quotaAndLimits.limitWriting.memProtection.dataNodeMemoryHighWaterLevel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>(0, 1], memoryHighWaterLevel in DataNodes</li>      </td>
      <td>0.95</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.memProtection.queryNodeMemoryLowWaterLevel`

<table id="quotaAndLimits.limitWriting.memProtection.queryNodeMemoryLowWaterLevel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>(0, 1], memoryLowWaterLevel in QueryNodes</li>      </td>
      <td>0.85</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.memProtection.queryNodeMemoryHighWaterLevel`

<table id="quotaAndLimits.limitWriting.memProtection.queryNodeMemoryHighWaterLevel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>(0, 1], memoryHighWaterLevel in QueryNodes</li>      </td>
      <td>0.95</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.growingSegmentsSizeProtection.enabled`

<table id="quotaAndLimits.limitWriting.growingSegmentsSizeProtection.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>No action will be taken if the growing segments size is less than the low watermark.</li>
        <li>When the growing segments size exceeds the low watermark, the dml rate will be reduced,</li>
        <li>but the rate will not be lower than minRateRatio * dmlRate.</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.growingSegmentsSizeProtection.minRateRatio`

<table id="quotaAndLimits.limitWriting.growingSegmentsSizeProtection.minRateRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0.5</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.growingSegmentsSizeProtection.lowWaterLevel`

<table id="quotaAndLimits.limitWriting.growingSegmentsSizeProtection.lowWaterLevel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0.2</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.growingSegmentsSizeProtection.highWaterLevel`

<table id="quotaAndLimits.limitWriting.growingSegmentsSizeProtection.highWaterLevel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0.4</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.diskProtection.enabled`

<table id="quotaAndLimits.limitWriting.diskProtection.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>When the total file size of object storage is greater than `diskQuota`, all dml requests would be rejected;</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.diskProtection.diskQuota`

<table id="quotaAndLimits.limitWriting.diskProtection.diskQuota">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB, (0, +inf), default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.diskProtection.diskQuotaPerDB`

<table id="quotaAndLimits.limitWriting.diskProtection.diskQuotaPerDB">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB, (0, +inf), default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.diskProtection.diskQuotaPerCollection`

<table id="quotaAndLimits.limitWriting.diskProtection.diskQuotaPerCollection">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB, (0, +inf), default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitWriting.diskProtection.diskQuotaPerPartition`

<table id="quotaAndLimits.limitWriting.diskProtection.diskQuotaPerPartition">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB, (0, +inf), default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.forceDeny`

<table id="quotaAndLimits.limitReading.forceDeny">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>forceDeny false means dql requests are allowed (except for some</li>
        <li>specific conditions, such as collection has been dropped), true means always reject all dql requests.</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.queueProtection.enabled`

<table id="quotaAndLimits.limitReading.queueProtection.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.queueProtection.nqInQueueThreshold`

<table id="quotaAndLimits.limitReading.queueProtection.nqInQueueThreshold">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>nqInQueueThreshold indicated that the system was under backpressure for Search/Query path.</li>
        <li>If NQ in any QueryNode's queue is greater than nqInQueueThreshold, search&query rates would gradually cool off</li>
        <li>until the NQ in queue no longer exceeds nqInQueueThreshold. We think of the NQ of query request as 1.</li>
        <li>int, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.queueProtection.queueLatencyThreshold`

<table id="quotaAndLimits.limitReading.queueProtection.queueLatencyThreshold">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>queueLatencyThreshold indicated that the system was under backpressure for Search/Query path.</li>
        <li>If dql latency of queuing is greater than queueLatencyThreshold, search&query rates would gradually cool off</li>
        <li>until the latency of queuing no longer exceeds queueLatencyThreshold.</li>
        <li>The latency here refers to the averaged latency over a period of time.</li>
        <li>milliseconds, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.resultProtection.enabled`

<table id="quotaAndLimits.limitReading.resultProtection.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.resultProtection.maxReadResultRate`

<table id="quotaAndLimits.limitReading.resultProtection.maxReadResultRate">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>maxReadResultRate indicated that the system was under backpressure for Search/Query path.</li>
        <li>If dql result rate is greater than maxReadResultRate, search&query rates would gradually cool off</li>
        <li>until the read result rate no longer exceeds maxReadResultRate.</li>
        <li>MB/s, default no limit</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.resultProtection.maxReadResultRatePerDB`

<table id="quotaAndLimits.limitReading.resultProtection.maxReadResultRatePerDB">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.resultProtection.maxReadResultRatePerCollection`

<table id="quotaAndLimits.limitReading.resultProtection.maxReadResultRatePerCollection">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `quotaAndLimits.limitReading.coolOffSpeed`

<table id="quotaAndLimits.limitReading.coolOffSpeed">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>colOffSpeed is the speed of search&query rates cool off.</li>
        <li>(0, 1]</li>      </td>
      <td>0.9</td>
    </tr>
  </tbody>
</table>


