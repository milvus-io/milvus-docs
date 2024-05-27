---
id: configure_trace.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure trace for Milvus.
---

# trace-related Configurations



## `trace.exporter`

<table id="trace.exporter">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>trace exporter type, default is stdout,</li>
        <li>optional values: ['noop','stdout', 'jaeger', 'otlp']</li>      </td>
      <td>noop</td>
    </tr>
  </tbody>
</table>


## `trace.sampleFraction`

<table id="trace.sampleFraction">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>fraction of traceID based sampler,</li>
        <li>optional values: [0, 1]</li>
        <li>Fractions >= 1 will always sample. Fractions < 0 are treated as zero.</li>      </td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## `trace.jaeger.url`

<table id="trace.jaeger.url">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>when exporter is jaeger should set the jaeger's URL</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `trace.otlp.endpoint`

<table id="trace.otlp.endpoint">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>example: "127.0.0.1:4318"</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `trace.otlp.secure`

<table id="trace.otlp.secure">
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


