---
id: configure_mq.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure mq for Milvus.
---

# mq-related Configurations

Milvus supports four MQ: rocksmq(based on RockDB), natsmq(embedded nats-server), Pulsar and Kafka.

You can change your mq by setting mq.type field.

If you don't set mq.type field as default, there is a note about enabling priority if we config multiple mq in this file.

1. standalone(local) mode: rocksmq(default) > natsmq > Pulsar > Kafka

2. cluster mode:  Pulsar(default) > Kafka (rocksmq and natsmq is unsupported in cluster mode)

## `mq.type`

<table id="mq.type">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Default value: "default"</li>
        <li>Valid values: [default, pulsar, kafka, rocksmq, natsmq]</li>      </td>
      <td>default</td>
    </tr>
  </tbody>
</table>


## `mq.enablePursuitMode`

<table id="mq.enablePursuitMode">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Default value: "true"</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


## `mq.pursuitLag`

<table id="mq.pursuitLag">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>time tick lag threshold to enter pursuit mode, in seconds</li>      </td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `mq.pursuitBufferSize`

<table id="mq.pursuitBufferSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>pursuit mode buffer size in bytes</li>      </td>
      <td>8388608</td>
    </tr>
  </tbody>
</table>


## `mq.mqBufSize`

<table id="mq.mqBufSize">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MQ client consumer buffer length</li>      </td>
      <td>16</td>
    </tr>
  </tbody>
</table>


