---
id: configure_rocksmq.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure rocksmq for Milvus.
---

# rocksmq-related Configurations

If you want to enable kafka, needs to comment the pulsar configs

kafka:

  brokerList: 

  saslUsername: 

  saslPassword: 

  saslMechanisms: 

  securityProtocol: 

  ssl:

    enabled: false # whether to enable ssl mode

    tlsCert:  # path to client's public key (PEM) used for authentication

    tlsKey:  # path to client's private key (PEM) used for authentication

    tlsCaCert:  # file or directory path to CA certificate(s) for verifying the broker's key

    tlsKeyPassword:  # private key passphrase for use with ssl.key.location and set_ssl_cert(), if any

  readTimeout: 10



## `rocksmq.path`

<table id="rocksmq.path">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The path where the message is stored in rocksmq</li>
        <li>please adjust in embedded Milvus: /tmp/milvus/rdb_data</li>      </td>
      <td>/var/lib/milvus/rdb_data</td>
    </tr>
  </tbody>
</table>


## `rocksmq.lrucacheratio`

<table id="rocksmq.lrucacheratio">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>rocksdb cache memory ratio</li>      </td>
      <td>0.06</td>
    </tr>
  </tbody>
</table>


## `rocksmq.rocksmqPageSize`

<table id="rocksmq.rocksmqPageSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>64 MB, 64 * 1024 * 1024 bytes, The size of each page of messages in rocksmq</li>      </td>
      <td>67108864</td>
    </tr>
  </tbody>
</table>


## `rocksmq.retentionTimeInMinutes`

<table id="rocksmq.retentionTimeInMinutes">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>3 days, 3 * 24 * 60 minutes, The retention time of the message in rocksmq.</li>      </td>
      <td>4320</td>
    </tr>
  </tbody>
</table>


## `rocksmq.retentionSizeInMB`

<table id="rocksmq.retentionSizeInMB">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>8 GB, 8 * 1024 MB, The retention size of the message in rocksmq.</li>      </td>
      <td>8192</td>
    </tr>
  </tbody>
</table>


## `rocksmq.compactionInterval`

<table id="rocksmq.compactionInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>1 day, trigger rocksdb compaction every day to remove deleted data</li>      </td>
      <td>86400</td>
    </tr>
  </tbody>
</table>


## `rocksmq.compressionTypes`

<table id="rocksmq.compressionTypes">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>compaction compression type, only support use 0,7. 0 means not compress, 7 will use zstd. Length of types means num of rocksdb level.</li>      </td>
      <td>0,0,7,7,7</td>
    </tr>
  </tbody>
</table>


