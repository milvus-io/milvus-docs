---
id: configure_indexnode.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure indexNode for Milvus.
---

# indexNode-related Configurations



## `indexNode.scheduler.buildParallel`

<table id="indexNode.scheduler.buildParallel">
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


## `indexNode.enableDisk`

<table id="indexNode.enableDisk">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>enable index node build disk vector index</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `indexNode.maxDiskUsagePercentage`

<table id="indexNode.maxDiskUsagePercentage">
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


## `indexNode.ip`

<table id="indexNode.ip">
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


## `indexNode.port`

<table id="indexNode.port">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>21121</td>
    </tr>
  </tbody>
</table>


## `indexNode.grpc.serverMaxSendSize`

<table id="indexNode.grpc.serverMaxSendSize">
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


## `indexNode.grpc.serverMaxRecvSize`

<table id="indexNode.grpc.serverMaxRecvSize">
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


## `indexNode.grpc.clientMaxSendSize`

<table id="indexNode.grpc.clientMaxSendSize">
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


## `indexNode.grpc.clientMaxRecvSize`

<table id="indexNode.grpc.clientMaxRecvSize">
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


