---
id: configure_datacoord.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure dataCoord for Milvus.
---

# dataCoord-related Configurations



## `dataCoord.channel.watchTimeoutInterval`

<table id="dataCoord.channel.watchTimeoutInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Timeout on watching channels (in seconds). Datanode tickler update watch progress will reset timeout timer.</li>      </td>
      <td>300</td>
    </tr>
  </tbody>
</table>


## `dataCoord.channel.balanceWithRpc`

<table id="dataCoord.channel.balanceWithRpc">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to enable balance with RPC, default to use etcd watch</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `dataCoord.channel.legacyVersionWithoutRPCWatch`

<table id="dataCoord.channel.legacyVersionWithoutRPCWatch">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Datanodes <= this version are considered as legacy nodes, which doesn't have rpc based watch(). This is only used during rolling upgrade where legacy nodes won't get new channels</li>      </td>
      <td>2.4.0</td>
    </tr>
  </tbody>
</table>


## `dataCoord.channel.balanceSilentDuration`

<table id="dataCoord.channel.balanceSilentDuration">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The duration after which the channel manager start background channel balancing</li>      </td>
      <td>300</td>
    </tr>
  </tbody>
</table>


## `dataCoord.channel.balanceInterval`

<table id="dataCoord.channel.balanceInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The interval with which the channel manager check dml channel balance status</li>      </td>
      <td>360</td>
    </tr>
  </tbody>
</table>


## `dataCoord.channel.checkInterval`

<table id="dataCoord.channel.checkInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The interval in seconds with which the channel manager advances channel states</li>      </td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## `dataCoord.channel.notifyChannelOperationTimeout`

<table id="dataCoord.channel.notifyChannelOperationTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Timeout notifing channel operations (in seconds).</li>      </td>
      <td>5</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.maxSize`

<table id="dataCoord.segment.maxSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum size of a segment in MB</li>      </td>
      <td>1024</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.diskSegmentMaxSize`

<table id="dataCoord.segment.diskSegmentMaxSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximun size of a segment in MB for collection which has Disk index</li>      </td>
      <td>2048</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.sealProportion`

<table id="dataCoord.segment.sealProportion">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0.12</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.assignmentExpiration`

<table id="dataCoord.segment.assignmentExpiration">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The time of the assignment expiration in ms</li>      </td>
      <td>2000</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.allocLatestExpireAttempt`

<table id="dataCoord.segment.allocLatestExpireAttempt">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The time attempting to alloc latest lastExpire from rootCoord after restart</li>      </td>
      <td>200</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.maxLife`

<table id="dataCoord.segment.maxLife">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The max lifetime of segment in seconds, 24*60*60</li>      </td>
      <td>86400</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.maxIdleTime`

<table id="dataCoord.segment.maxIdleTime">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>If a segment didn't accept dml records in maxIdleTime and the size of segment is greater than</li>
        <li>minSizeFromIdleToSealed, Milvus will automatically seal it.</li>
        <li>The max idle time of segment in seconds, 10*60.</li>      </td>
      <td>600</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.minSizeFromIdleToSealed`

<table id="dataCoord.segment.minSizeFromIdleToSealed">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The min size in MB of segment which can be idle from sealed.</li>      </td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.maxBinlogFileNumber`

<table id="dataCoord.segment.maxBinlogFileNumber">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The max number of binlog file for one segment, the segment will be sealed if</li>
        <li>the number of binlog file reaches to max value.</li>      </td>
      <td>32</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.smallProportion`

<table id="dataCoord.segment.smallProportion">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The segment is considered as "small segment" when its # of rows is smaller than</li>      </td>
      <td>0.5</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.compactableProportion`

<table id="dataCoord.segment.compactableProportion">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>(smallProportion * segment max # of rows).</li>
        <li>A compaction will happen on small segments if the segment after compaction will have</li>      </td>
      <td>0.85</td>
    </tr>
  </tbody>
</table>


## `dataCoord.segment.expansionRate`

<table id="dataCoord.segment.expansionRate">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>over (compactableProportion * segment max # of rows) rows.</li>
        <li>MUST BE GREATER THAN OR EQUAL TO <smallProportion>!!!</li>
        <li>During compaction, the size of segment # of rows is able to exceed segment max # of rows by (expansionRate-1) * 100%. </li>      </td>
      <td>1.25</td>
    </tr>
  </tbody>
</table>


## `dataCoord.autoUpgradeSegmentIndex`

<table id="dataCoord.autoUpgradeSegmentIndex">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>whether auto upgrade segment index to index engine's version</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `dataCoord.enableCompaction`

<table id="dataCoord.enableCompaction">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Enable data segment compaction</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `dataCoord.compaction.enableAutoCompaction`

<table id="dataCoord.compaction.enableAutoCompaction">
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


## `dataCoord.compaction.indexBasedCompaction`

<table id="dataCoord.compaction.indexBasedCompaction">
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


## `dataCoord.compaction.rpcTimeout`

<table id="dataCoord.compaction.rpcTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `dataCoord.compaction.maxParallelTaskNum`

<table id="dataCoord.compaction.maxParallelTaskNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `dataCoord.compaction.workerMaxParallelTaskNum`

<table id="dataCoord.compaction.workerMaxParallelTaskNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>2</td>
    </tr>
  </tbody>
</table>


## `dataCoord.compaction.levelzero.forceTrigger.minSize`

<table id="dataCoord.compaction.levelzero.forceTrigger.minSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The minmum size in bytes to force trigger a LevelZero Compaction, default as 8MB</li>      </td>
      <td>8388608</td>
    </tr>
  </tbody>
</table>


## `dataCoord.compaction.levelzero.forceTrigger.maxSize`

<table id="dataCoord.compaction.levelzero.forceTrigger.maxSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The maxmum size in bytes to force trigger a LevelZero Compaction, default as 64MB</li>      </td>
      <td>67108864</td>
    </tr>
  </tbody>
</table>


## `dataCoord.compaction.levelzero.forceTrigger.deltalogMinNum`

<table id="dataCoord.compaction.levelzero.forceTrigger.deltalogMinNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The minimum number of deltalog files to force trigger a LevelZero Compaction</li>      </td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `dataCoord.compaction.levelzero.forceTrigger.deltalogMaxNum`

<table id="dataCoord.compaction.levelzero.forceTrigger.deltalogMaxNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The maxmum number of deltalog files to force trigger a LevelZero Compaction, default as 30</li>      </td>
      <td>30</td>
    </tr>
  </tbody>
</table>


## `dataCoord.enableGarbageCollection`

<table id="dataCoord.enableGarbageCollection">
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


## `dataCoord.gc.interval`

<table id="dataCoord.gc.interval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>gc interval in seconds</li>      </td>
      <td>3600</td>
    </tr>
  </tbody>
</table>


## `dataCoord.gc.missingTolerance`

<table id="dataCoord.gc.missingTolerance">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>file meta missing tolerance duration in seconds, default to 24hr(1d)</li>      </td>
      <td>86400</td>
    </tr>
  </tbody>
</table>


## `dataCoord.gc.dropTolerance`

<table id="dataCoord.gc.dropTolerance">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>file belongs to dropped entity tolerance duration in seconds. 3600</li>      </td>
      <td>10800</td>
    </tr>
  </tbody>
</table>


## `dataCoord.gc.removeConcurrent`

<table id="dataCoord.gc.removeConcurrent">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>number of concurrent goroutines to remove dropped s3 objects</li>      </td>
      <td>32</td>
    </tr>
  </tbody>
</table>


## `dataCoord.gc.scanInterval`

<table id="dataCoord.gc.scanInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>garbage collection scan residue interval in hours</li>      </td>
      <td>168</td>
    </tr>
  </tbody>
</table>


## `dataCoord.enableActiveStandby`

<table id="dataCoord.enableActiveStandby">
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


## `dataCoord.brokerTimeout`

<table id="dataCoord.brokerTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>5000ms, dataCoord broker rpc timeout</li>      </td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## `dataCoord.autoBalance`

<table id="dataCoord.autoBalance">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Enable auto balance</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `dataCoord.checkAutoBalanceConfigInterval`

<table id="dataCoord.checkAutoBalanceConfigInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the interval of check auto balance config</li>      </td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `dataCoord.import.filesPerPreImportTask`

<table id="dataCoord.import.filesPerPreImportTask">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The maximum number of files allowed per pre-import task.</li>      </td>
      <td>2</td>
    </tr>
  </tbody>
</table>


## `dataCoord.import.taskRetention`

<table id="dataCoord.import.taskRetention">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The retention period in seconds for tasks in the Completed or Failed state.</li>      </td>
      <td>10800</td>
    </tr>
  </tbody>
</table>


## `dataCoord.import.maxSizeInMBPerImportTask`

<table id="dataCoord.import.maxSizeInMBPerImportTask">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>To prevent generating of small segments, we will re-group imported files. This parameter represents the sum of file sizes in each group (each ImportTask).</li>      </td>
      <td>6144</td>
    </tr>
  </tbody>
</table>


## `dataCoord.import.scheduleInterval`

<table id="dataCoord.import.scheduleInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The interval for scheduling import, measured in seconds.</li>      </td>
      <td>2</td>
    </tr>
  </tbody>
</table>


## `dataCoord.import.checkIntervalHigh`

<table id="dataCoord.import.checkIntervalHigh">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The interval for checking import, measured in seconds, is set to a high frequency for the import checker.</li>      </td>
      <td>2</td>
    </tr>
  </tbody>
</table>


## `dataCoord.import.checkIntervalLow`

<table id="dataCoord.import.checkIntervalLow">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The interval for checking import, measured in seconds, is set to a low frequency for the import checker.</li>      </td>
      <td>120</td>
    </tr>
  </tbody>
</table>


## `dataCoord.import.maxImportFileNumPerReq`

<table id="dataCoord.import.maxImportFileNumPerReq">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The maximum number of files allowed per single import request.</li>      </td>
      <td>1024</td>
    </tr>
  </tbody>
</table>


## `dataCoord.import.waitForIndex`

<table id="dataCoord.import.waitForIndex">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Indicates whether the import operation waits for the completion of index building.</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `dataCoord.gracefulStopTimeout`

<table id="dataCoord.gracefulStopTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>seconds. force stop node without graceful stop</li>      </td>
      <td>5</td>
    </tr>
  </tbody>
</table>


## `dataCoord.ip`

<table id="dataCoord.ip">
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


## `dataCoord.port`

<table id="dataCoord.port">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>13333</td>
    </tr>
  </tbody>
</table>


## `dataCoord.grpc.serverMaxSendSize`

<table id="dataCoord.grpc.serverMaxSendSize">
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


## `dataCoord.grpc.serverMaxRecvSize`

<table id="dataCoord.grpc.serverMaxRecvSize">
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


## `dataCoord.grpc.clientMaxSendSize`

<table id="dataCoord.grpc.clientMaxSendSize">
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


## `dataCoord.grpc.clientMaxRecvSize`

<table id="dataCoord.grpc.clientMaxRecvSize">
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


