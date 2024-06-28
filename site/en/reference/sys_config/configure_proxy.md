---
id: configure_proxy.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure proxy for Milvus.
---

# proxy-related Configurations

Related configuration of proxy, used to validate client requests and reduce the returned results.

## `proxy.timeTickInterval`

<table id="proxy.timeTickInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>ms, the interval that proxy synchronize the time tick</li>      </td>
      <td>200</td>
    </tr>
  </tbody>
</table>


## `proxy.healthCheckTimeout`

<table id="proxy.healthCheckTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>ms, the interval that to do component healthy check</li>      </td>
      <td>3000</td>
    </tr>
  </tbody>
</table>


## `proxy.msgStream.timeTick.bufSize`

<table id="proxy.msgStream.timeTick.bufSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>512</td>
    </tr>
  </tbody>
</table>


## `proxy.maxNameLength`

<table id="proxy.maxNameLength">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum length of name for a collection or alias</li>      </td>
      <td>255</td>
    </tr>
  </tbody>
</table>


## `proxy.maxFieldNum`

<table id="proxy.maxFieldNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum number of fields in a collection.</li>
        <li>As of today (2.2.0 and after) it is strongly DISCOURAGED to set maxFieldNum >= 64.</li>
        <li>So adjust at your risk!</li>      </td>
      <td>64</td>
    </tr>
  </tbody>
</table>


## `proxy.maxVectorFieldNum`

<table id="proxy.maxVectorFieldNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum number of vector fields in a collection.</li>      </td>
      <td>4</td>
    </tr>
  </tbody>
</table>


## `proxy.maxShardNum`

<table id="proxy.maxShardNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum number of shards in a collection</li>      </td>
      <td>16</td>
    </tr>
  </tbody>
</table>


## `proxy.maxDimension`

<table id="proxy.maxDimension">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum dimension of a vector</li>      </td>
      <td>32768</td>
    </tr>
  </tbody>
</table>


## `proxy.ginLogging`

<table id="proxy.ginLogging">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to produce gin logs.\n</li>
        <li>please adjust in embedded Milvus: false</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `proxy.ginLogSkipPaths`

<table id="proxy.ginLogSkipPaths">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>skip url path for gin log</li>      </td>
      <td>/</td>
    </tr>
  </tbody>
</table>


## `proxy.maxTaskNum`

<table id="proxy.maxTaskNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>max task number of proxy task queue</li>      </td>
      <td>1024</td>
    </tr>
  </tbody>
</table>


## `proxy.mustUsePartitionKey`

<table id="proxy.mustUsePartitionKey">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>switch for whether proxy must use partition key for the collection</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.enable`

<table id="proxy.accessLog.enable">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>if use access log</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.minioEnable`

<table id="proxy.accessLog.minioEnable">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>if upload sealed access log file to minio</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.localPath`

<table id="proxy.accessLog.localPath">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>/tmp/milvus_access</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.filename`

<table id="proxy.accessLog.filename">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Log filename, leave empty to use stdout.</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.maxSize`

<table id="proxy.accessLog.maxSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Max size for a single file, in MB.</li>      </td>
      <td>64</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.cacheSize`

<table id="proxy.accessLog.cacheSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Size of log of memory cache, in B</li>      </td>
      <td>10240</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.rotatedTime`

<table id="proxy.accessLog.rotatedTime">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Max time for single access log file in seconds</li>      </td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.remotePath`

<table id="proxy.accessLog.remotePath">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>File path in minIO</li>      </td>
      <td>access_log/</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.remoteMaxTime`

<table id="proxy.accessLog.remoteMaxTime">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Max time for log file in minIO, in hours</li>      </td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.formatters.base.format`

<table id="proxy.accessLog.formatters.base.format">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>[$time_now] [ACCESS] <$user_name: $user_addr> $method_name [status: $method_status] [code: $error_code] [sdk: $sdk_version] [msg: $error_msg] [traceID: $trace_id] [timeCost: $time_cost]</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.formatters.query.format`

<table id="proxy.accessLog.formatters.query.format">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>[$time_now] [ACCESS] <$user_name: $user_addr> $method_name [status: $method_status] [code: $error_code] [sdk: $sdk_version] [msg: $error_msg] [traceID: $trace_id] [timeCost: $time_cost] [database: $database_name] [collection: $collection_name] [partitions: $partition_name] [expr: $method_expr]</td>
    </tr>
  </tbody>
</table>


## `proxy.accessLog.formatters.query.methods`

<table id="proxy.accessLog.formatters.query.methods">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>Query,Search,Delete</td>
    </tr>
  </tbody>
</table>


## `proxy.connectionCheckIntervalSeconds`

<table id="proxy.connectionCheckIntervalSeconds">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the interval time(in seconds) for connection manager to scan inactive client info</li>      </td>
      <td>120</td>
    </tr>
  </tbody>
</table>


## `proxy.connectionClientInfoTTLSeconds`

<table id="proxy.connectionClientInfoTTLSeconds">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>inactive client info TTL duration, in seconds</li>      </td>
      <td>86400</td>
    </tr>
  </tbody>
</table>


## `proxy.maxConnectionNum`

<table id="proxy.maxConnectionNum">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>the max client info numbers that proxy should manage, avoid too many client infos</li>      </td>
      <td>10000</td>
    </tr>
  </tbody>
</table>


## `proxy.gracefulStopTimeout`

<table id="proxy.gracefulStopTimeout">
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
      <td>30</td>
    </tr>
  </tbody>
</table>


## `proxy.slowQuerySpanInSeconds`

<table id="proxy.slowQuerySpanInSeconds">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>query whose executed time exceeds the `slowQuerySpanInSeconds` can be considered slow, in seconds.</li>      </td>
      <td>5</td>
    </tr>
  </tbody>
</table>


## `proxy.http.enabled`

<table id="proxy.http.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to enable the http server</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `proxy.http.debug_mode`

<table id="proxy.http.debug_mode">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to enable http server debug mode</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `proxy.http.port`

<table id="proxy.http.port">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>high-level restful api</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `proxy.http.acceptTypeAllowInt64`

<table id="proxy.http.acceptTypeAllowInt64">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>high-level restful api, whether http client can deal with int64</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `proxy.http.enablePprof`

<table id="proxy.http.enablePprof">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to enable pprof middleware on the metrics port</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `proxy.ip`

<table id="proxy.ip">
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


## `proxy.port`

<table id="proxy.port">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>19530</td>
    </tr>
  </tbody>
</table>


## `proxy.internalPort`

<table id="proxy.internalPort">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>19529</td>
    </tr>
  </tbody>
</table>


## `proxy.grpc.serverMaxSendSize`

<table id="proxy.grpc.serverMaxSendSize">
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


## `proxy.grpc.serverMaxRecvSize`

<table id="proxy.grpc.serverMaxRecvSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>67108864</td>
    </tr>
  </tbody>
</table>


## `proxy.grpc.clientMaxSendSize`

<table id="proxy.grpc.clientMaxSendSize">
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


## `proxy.grpc.clientMaxRecvSize`

<table id="proxy.grpc.clientMaxRecvSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>67108864</td>
    </tr>
  </tbody>
</table>


