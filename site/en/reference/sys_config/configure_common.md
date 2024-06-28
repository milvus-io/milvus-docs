---
id: configure_common.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure common for Milvus.
---

# common-related Configurations



## `common.defaultPartitionName`

<table id="common.defaultPartitionName">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>default partition name for a collection</li>      </td>
      <td>_default</td>
    </tr>
  </tbody>
</table>


## `common.defaultIndexName`

<table id="common.defaultIndexName">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>default index name</li>      </td>
      <td>_default_idx</td>
    </tr>
  </tbody>
</table>


## `common.entityExpiration`

<table id="common.entityExpiration">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Entity expiration in seconds, CAUTION -1 means never expire</li>      </td>
      <td>-1</td>
    </tr>
  </tbody>
</table>


## `common.indexSliceSize`

<table id="common.indexSliceSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MB</li>      </td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## `common.threadCoreCoefficient.highPriority`

<table id="common.threadCoreCoefficient.highPriority">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>This parameter specify how many times the number of threads is the number of cores in high priority pool</li>      </td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `common.threadCoreCoefficient.middlePriority`

<table id="common.threadCoreCoefficient.middlePriority">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>This parameter specify how many times the number of threads is the number of cores in middle priority pool</li>      </td>
      <td>5</td>
    </tr>
  </tbody>
</table>


## `common.threadCoreCoefficient.lowPriority`

<table id="common.threadCoreCoefficient.lowPriority">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>This parameter specify how many times the number of threads is the number of cores in low priority pool</li>      </td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## `common.buildIndexThreadPoolRatio`

<table id="common.buildIndexThreadPoolRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0.75</td>
    </tr>
  </tbody>
</table>


## `common.DiskIndex.MaxDegree`

<table id="common.DiskIndex.MaxDegree">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>56</td>
    </tr>
  </tbody>
</table>


## `common.DiskIndex.SearchListSize`

<table id="common.DiskIndex.SearchListSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>100</td>
    </tr>
  </tbody>
</table>


## `common.DiskIndex.PQCodeBudgetGBRatio`

<table id="common.DiskIndex.PQCodeBudgetGBRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0.125</td>
    </tr>
  </tbody>
</table>


## `common.DiskIndex.BuildNumThreadsRatio`

<table id="common.DiskIndex.BuildNumThreadsRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>1</td>
    </tr>
  </tbody>
</table>


## `common.DiskIndex.SearchCacheBudgetGBRatio`

<table id="common.DiskIndex.SearchCacheBudgetGBRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0.1</td>
    </tr>
  </tbody>
</table>


## `common.DiskIndex.LoadNumThreadRatio`

<table id="common.DiskIndex.LoadNumThreadRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>8</td>
    </tr>
  </tbody>
</table>


## `common.DiskIndex.BeamWidthRatio`

<table id="common.DiskIndex.BeamWidthRatio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>4</td>
    </tr>
  </tbody>
</table>


## `common.gracefulTime`

<table id="common.gracefulTime">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>milliseconds. it represents the interval (in ms) by which the request arrival time needs to be subtracted in the case of Bounded Consistency.</li>      </td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## `common.gracefulStopTimeout`

<table id="common.gracefulStopTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>seconds. it will force quit the server if the graceful stop process is not completed during this time.</li>      </td>
      <td>1800</td>
    </tr>
  </tbody>
</table>


## `common.storageType`

<table id="common.storageType">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>please adjust in embedded Milvus: local, available values are [local, remote, opendal], value minio is deprecated, use remote instead</li>      </td>
      <td>remote</td>
    </tr>
  </tbody>
</table>


## `common.simdType`

<table id="common.simdType">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Default value: auto</li>
        <li>Valid values: [auto, avx512, avx2, avx, sse4_2]</li>
        <li>This configuration is only used by querynode and indexnode, it selects CPU instruction set for Searching and Index-building.</li>      </td>
      <td>auto</td>
    </tr>
  </tbody>
</table>


## `common.security.authorizationEnabled`

<table id="common.security.authorizationEnabled">
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


## `common.security.superUsers`

<table id="common.security.superUsers">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The superusers will ignore some system check processes,</li>
        <li>like the old password verification when updating the credential</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `common.security.tlsMode`

<table id="common.security.tlsMode">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## `common.session.ttl`

<table id="common.session.ttl">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>ttl value when session granting a lease to register service</li>      </td>
      <td>30</td>
    </tr>
  </tbody>
</table>


## `common.session.retryTimes`

<table id="common.session.retryTimes">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>retry times when session sending etcd requests</li>      </td>
      <td>30</td>
    </tr>
  </tbody>
</table>


## `common.locks.metrics.enable`

<table id="common.locks.metrics.enable">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>whether gather statistics for metrics locks</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `common.locks.threshold.info`

<table id="common.locks.threshold.info">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>minimum milliseconds for printing durations in info level</li>      </td>
      <td>500</td>
    </tr>
  </tbody>
</table>


## `common.locks.threshold.warn`

<table id="common.locks.threshold.warn">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>minimum milliseconds for printing durations in warn level</li>      </td>
      <td>1000</td>
    </tr>
  </tbody>
</table>


## `common.storage.scheme`

<table id="common.storage.scheme">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>s3</td>
    </tr>
  </tbody>
</table>


## `common.storage.enablev2`

<table id="common.storage.enablev2">
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


## `common.ttMsgEnabled`

<table id="common.ttMsgEnabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether the instance disable sending ts messages</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `common.traceLogMode`

<table id="common.traceLogMode">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>trace request info</li>      </td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## `common.bloomFilterSize`

<table id="common.bloomFilterSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>bloom filter initial size</li>      </td>
      <td>100000</td>
    </tr>
  </tbody>
</table>


## `common.maxBloomFalsePositive`

<table id="common.maxBloomFalsePositive">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>max false positive rate for bloom filter</li>      </td>
      <td>0.001</td>
    </tr>
  </tbody>
</table>


