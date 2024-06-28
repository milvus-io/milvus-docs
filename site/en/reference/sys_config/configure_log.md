---
id: configure_log.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure log for Milvus.
---

# log-related Configurations

Configures the system log output.

## `log.level`

<table id="log.level">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Only supports debug, info, warn, error, panic, or fatal. Default 'info'.</li>      </td>
      <td>info</td>
    </tr>
  </tbody>
</table>


## `log.file.rootPath`

<table id="log.file.rootPath">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>root dir path to put logs, default "" means no log file will print. please adjust in embedded Milvus: /tmp/milvus/logs</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `log.file.maxSize`

<table id="log.file.maxSize">
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
      <td>300</td>
    </tr>
  </tbody>
</table>


## `log.file.maxAge`

<table id="log.file.maxAge">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Maximum time for log retention in day.</li>      </td>
      <td>10</td>
    </tr>
  </tbody>
</table>


## `log.file.maxBackups`

<table id="log.file.maxBackups">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>20</td>
    </tr>
  </tbody>
</table>


## `log.format`

<table id="log.format">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>text or json</li>      </td>
      <td>text</td>
    </tr>
  </tbody>
</table>


## `log.stdout`

<table id="log.stdout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Stdout enable or not</li>      </td>
      <td>true</td>
    </tr>
  </tbody>
</table>


