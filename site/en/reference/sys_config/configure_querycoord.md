---
id: configure_querycoord.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure queryCoord for Milvus.
---

# queryCoord-related Configurations

Related configuration of queryCoord, used to manage topology and load balancing for the query nodes, and handoff from growing segments to sealed segments.

## `queryCoord.taskMergeCap`

<table id="queryCoord.taskMergeCap">
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


## `queryCoord.taskExecutionCap`

<table id="queryCoord.taskExecutionCap">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>256</td>
    </tr>
  </tbody>
</table>


## `queryCoord.autoHandoff`

<table id="queryCoord.autoHandoff">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Enable auto handoff</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `queryCoord.autoBalance`

<table id="queryCoord.autoBalance">
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


## `queryCoord.autoBalanceChannel`

<table id="queryCoord.autoBalanceChannel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Enable auto balance channel</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `queryCoord.balancer`

<table id="queryCoord.balancer">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>auto balancer used for segments on queryNodes</li>      </td>
      <td>ScoreBasedBalancer</td>
    </tr>
  </tbody>
</table>


## `queryCoord.globalRowCountFactor`

<table id="queryCoord.globalRowCountFactor">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the weight used when balancing segments among queryNodes</li>      </td>
      <td>0.1</td>
    </tr>
  </tbody>
</table>


## `queryCoord.scoreUnbalanceTolerationFactor`

<table id="queryCoord.scoreUnbalanceTolerationFactor">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the least value for unbalanced extent between from and to nodes when doing balance</li>      </td>
      <td>0.05</td>
    </tr>
  </tbody>
</table>


## `queryCoord.reverseUnBalanceTolerationFactor`

<table id="queryCoord.reverseUnBalanceTolerationFactor">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the largest value for unbalanced extent between from and to nodes after doing balance</li>      </td>
      <td>1.3</td>
    </tr>
  </tbody>
</table>


## `queryCoord.overloadedMemoryThresholdPercentage`

<table id="queryCoord.overloadedMemoryThresholdPercentage">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The threshold percentage that memory overload</li>      </td>
      <td>90</td>
    </tr>
  </tbody>
</table>


## `queryCoord.balanceIntervalSeconds`

<table id="queryCoord.balanceIntervalSeconds">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>60</td>
    </tr>
  </tbody>
</table>


## `queryCoord.memoryUsageMaxDifferencePercentage`

<table id="queryCoord.memoryUsageMaxDifferencePercentage">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>30</td>
    </tr>
  </tbody>
</table>


## `queryCoord.rowCountFactor`

<table id="queryCoord.rowCountFactor">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the row count weight used when balancing segments among queryNodes</li>      </td>
      <td>0.4</td>
    </tr>
  </tbody>
</table>


## `queryCoord.segmentCountFactor`

<table id="queryCoord.segmentCountFactor">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the segment count weight used when balancing segments among queryNodes</li>      </td>
      <td>0.4</td>
    </tr>
  </tbody>
</table>


## `queryCoord.globalSegmentCountFactor`

<table id="queryCoord.globalSegmentCountFactor">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the segment count weight used when balancing segments among queryNodes</li>      </td>
      <td>0.1</td>
    </tr>
  </tbody>
</table>


## `queryCoord.segmentCountMaxSteps`

<table id="queryCoord.segmentCountMaxSteps">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>segment count based plan generator max steps</li>      </td>
      <td>50</td>
    </tr>
  </tbody>
</table>


## `queryCoord.rowCountMaxSteps`

<table id="queryCoord.rowCountMaxSteps">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>segment count based plan generator max steps</li>      </td>
      <td>50</td>
    </tr>
  </tbody>
</table>


## `queryCoord.randomMaxSteps`

<table id="queryCoord.randomMaxSteps">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>segment count based plan generator max steps</li>      </td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `queryCoord.growingRowCountWeight`

<table id="queryCoord.growingRowCountWeight">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the memory weight of growing segment row count</li>      </td>
      <td>4</td>
    </tr>
  </tbody>
</table>


## `queryCoord.balanceCostThreshold`

<table id="queryCoord.balanceCostThreshold">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the threshold of balance cost, if the difference of cluster's cost after executing the balance plan is less than this value, the plan will not be executed</li>      </td>
      <td>0.001</td>
    </tr>
  </tbody>
</table>


## `queryCoord.checkSegmentInterval`

<table id="queryCoord.checkSegmentInterval">
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


## `queryCoord.checkChannelInterval`

<table id="queryCoord.checkChannelInterval">
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


## `queryCoord.checkBalanceInterval`

<table id="queryCoord.checkBalanceInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>10000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.checkIndexInterval`

<table id="queryCoord.checkIndexInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>10000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.channelTaskTimeout`

<table id="queryCoord.channelTaskTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>1 minute</li>      </td>
      <td>60000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.segmentTaskTimeout`

<table id="queryCoord.segmentTaskTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>2 minute</li>      </td>
      <td>120000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.distPullInterval`

<table id="queryCoord.distPullInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>500</td>
    </tr>
  </tbody>
</table>


## `queryCoord.heartbeatAvailableInterval`

<table id="queryCoord.heartbeatAvailableInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>10s, Only QueryNodes which fetched heartbeats within the duration are available</li>      </td>
      <td>10000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.loadTimeoutSeconds`

<table id="queryCoord.loadTimeoutSeconds">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>600</td>
    </tr>
  </tbody>
</table>


## `queryCoord.distRequestTimeout`

<table id="queryCoord.distRequestTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the request timeout for querycoord fetching data distribution from querynodes, in milliseconds</li>      </td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.heatbeatWarningLag`

<table id="queryCoord.heatbeatWarningLag">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the lag value for querycoord report warning when last heatbeat is too old, in milliseconds</li>      </td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.checkHandoffInterval`

<table id="queryCoord.checkHandoffInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.enableActiveStandby`

<table id="queryCoord.enableActiveStandby">
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


## `queryCoord.checkInterval`

<table id="queryCoord.checkInterval">
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


## `queryCoord.checkHealthInterval`

<table id="queryCoord.checkHealthInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>3s, the interval when query coord try to check health of query node</li>      </td>
      <td>3000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.checkHealthRPCTimeout`

<table id="queryCoord.checkHealthRPCTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>100ms, the timeout of check health rpc to query node</li>      </td>
      <td>2000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.brokerTimeout`

<table id="queryCoord.brokerTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>5000ms, querycoord broker rpc timeout</li>      </td>
      <td>5000</td>
    </tr>
  </tbody>
</table>


## `queryCoord.collectionRecoverTimes`

<table id="queryCoord.collectionRecoverTimes">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>if collection recover times reach the limit during loading state, release it</li>      </td>
      <td>3</td>
    </tr>
  </tbody>
</table>


## `queryCoord.observerTaskParallel`

<table id="queryCoord.observerTaskParallel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the parallel observer dispatcher task number</li>      </td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## `queryCoord.checkAutoBalanceConfigInterval`

<table id="queryCoord.checkAutoBalanceConfigInterval">
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


## `queryCoord.checkNodeSessionInterval`

<table id="queryCoord.checkNodeSessionInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the interval(in seconds) of check querynode cluster session</li>      </td>
      <td>60</td>
    </tr>
  </tbody>
</table>


## `queryCoord.gracefulStopTimeout`

<table id="queryCoord.gracefulStopTimeout">
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


## `queryCoord.enableStoppingBalance`

<table id="queryCoord.enableStoppingBalance">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>whether enable stopping balance</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `queryCoord.channelExclusiveNodeFactor`

<table id="queryCoord.channelExclusiveNodeFactor">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the least node number for enable channel's exclusive mode</li>      </td>
      <td>4</td>
    </tr>
  </tbody>
</table>


## `queryCoord.cleanExcludeSegmentInterval`

<table id="queryCoord.cleanExcludeSegmentInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the time duration of clean pipeline exclude segment which used for filter invalid data, in seconds</li>      </td>
      <td>60</td>
    </tr>
  </tbody>
</table>


## `queryCoord.ip`

<table id="queryCoord.ip">
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


## `queryCoord.port`

<table id="queryCoord.port">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>19531</td>
    </tr>
  </tbody>
</table>


## `queryCoord.grpc.serverMaxSendSize`

<table id="queryCoord.grpc.serverMaxSendSize">
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


## `queryCoord.grpc.serverMaxRecvSize`

<table id="queryCoord.grpc.serverMaxRecvSize">
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


## `queryCoord.grpc.clientMaxSendSize`

<table id="queryCoord.grpc.clientMaxSendSize">
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


## `queryCoord.grpc.clientMaxRecvSize`

<table id="queryCoord.grpc.clientMaxRecvSize">
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


