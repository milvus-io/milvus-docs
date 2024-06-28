---
id: configure_pulsar.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure pulsar for Milvus.
---

# pulsar-related Configurations

Related configuration of pulsar, used to manage Milvus logs of recent mutation operations, output streaming log, and provide log publish-subscribe services.

## `pulsar.address`

<table id="pulsar.address">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Address of pulsar</li>      </td>
      <td>localhost</td>
    </tr>
  </tbody>
</table>


## `pulsar.port`

<table id="pulsar.port">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Port of Pulsar</li>      </td>
      <td>6650</td>
    </tr>
  </tbody>
</table>


## `pulsar.webport`

<table id="pulsar.webport">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Web port of pulsar, if you connect directly without proxy, should use 8080</li>      </td>
      <td>80</td>
    </tr>
  </tbody>
</table>


## `pulsar.maxMessageSize`

<table id="pulsar.maxMessageSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>5 * 1024 * 1024 Bytes, Maximum size of each message in pulsar.</li>      </td>
      <td>5242880</td>
    </tr>
  </tbody>
</table>


## `pulsar.tenant`

<table id="pulsar.tenant">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>public</td>
    </tr>
  </tbody>
</table>


## `pulsar.namespace`

<table id="pulsar.namespace">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>default</td>
    </tr>
  </tbody>
</table>


## `pulsar.requestTimeout`

<table id="pulsar.requestTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>pulsar client global request timeout in seconds</li>      </td>
      <td>60</td>
    </tr>
  </tbody>
</table>


## `pulsar.enableClientMetrics`

<table id="pulsar.enableClientMetrics">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to register pulsar client metrics into milvus metrics path.</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


