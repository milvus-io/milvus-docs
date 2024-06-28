---
id: configure_grpc.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure grpc for Milvus.
---

# grpc-related Configurations



## `grpc.log.level`

<table id="grpc.log.level">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>WARNING</td>
    </tr>
  </tbody>
</table>


## `grpc.gracefulStopTimeout`

<table id="grpc.gracefulStopTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>second, time to wait graceful stop finish</li>      </td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `grpc.client.compressionEnabled`

<table id="grpc.client.compressionEnabled">
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


## `grpc.client.dialTimeout`

<table id="grpc.client.dialTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>200</td>
    </tr>
  </tbody>
</table>


## `grpc.client.keepAliveTime`

<table id="grpc.client.keepAliveTime">
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


## `grpc.client.keepAliveTimeout`

<table id="grpc.client.keepAliveTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>20000</td>
    </tr>
  </tbody>
</table>


## `grpc.client.maxMaxAttempts`

<table id="grpc.client.maxMaxAttempts">
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


## `grpc.client.initialBackoff`

<table id="grpc.client.initialBackoff">
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


## `grpc.client.maxBackoff`

<table id="grpc.client.maxBackoff">
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


## `grpc.client.minResetInterval`

<table id="grpc.client.minResetInterval">
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


## `grpc.client.maxCancelError`

<table id="grpc.client.maxCancelError">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>32</td>
    </tr>
  </tbody>
</table>


## `grpc.client.minSessionCheckInterval`

<table id="grpc.client.minSessionCheckInterval">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>200</td>
    </tr>
  </tbody>
</table>


