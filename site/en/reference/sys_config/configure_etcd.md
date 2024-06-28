---
id: configure_etcd.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure etcd for Milvus.
---

# etcd-related Configurations

Related configuration of etcd, used to store Milvus metadata & service discovery.

## `etcd.endpoints`

<table id="etcd.endpoints">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>localhost:2379</td>
    </tr>
  </tbody>
</table>


## `etcd.rootPath`

<table id="etcd.rootPath">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The root path where data is stored in etcd</li>      </td>
      <td>by-dev</td>
    </tr>
  </tbody>
</table>


## `etcd.metaSubPath`

<table id="etcd.metaSubPath">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>metaRootPath = rootPath + '/' + metaSubPath</li>      </td>
      <td>meta</td>
    </tr>
  </tbody>
</table>


## `etcd.kvSubPath`

<table id="etcd.kvSubPath">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>kvRootPath = rootPath + '/' + kvSubPath</li>      </td>
      <td>kv</td>
    </tr>
  </tbody>
</table>


## `etcd.log.level`

<table id="etcd.log.level">
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


## `etcd.log.path`

<table id="etcd.log.path">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>path is one of:</li>
        <li> - "default" as os.Stderr,</li>
        <li> - "stderr" as os.Stderr,</li>
        <li> - "stdout" as os.Stdout,</li>
        <li> - file path to append server logs to.</li>
        <li>please adjust in embedded Milvus: /tmp/milvus/logs/etcd.log</li>      </td>
      <td>stdout</td>
    </tr>
  </tbody>
</table>


## `etcd.ssl.enabled`

<table id="etcd.ssl.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to support ETCD secure connection mode</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `etcd.ssl.tlsCert`

<table id="etcd.ssl.tlsCert">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>path to your cert file</li>      </td>
      <td>/path/to/etcd-client.pem</td>
    </tr>
  </tbody>
</table>


## `etcd.ssl.tlsKey`

<table id="etcd.ssl.tlsKey">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>path to your key file</li>      </td>
      <td>/path/to/etcd-client-key.pem</td>
    </tr>
  </tbody>
</table>


## `etcd.ssl.tlsCACert`

<table id="etcd.ssl.tlsCACert">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>path to your CACert file</li>      </td>
      <td>/path/to/ca.pem</td>
    </tr>
  </tbody>
</table>


## `etcd.ssl.tlsMinVersion`

<table id="etcd.ssl.tlsMinVersion">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>TLS min version</li>
        <li>Optional values: 1.0, 1.1, 1.2, 1.3。</li>
        <li>We recommend using version 1.2 and above.</li>      </td>
      <td>1.3</td>
    </tr>
  </tbody>
</table>


## `etcd.requestTimeout`

<table id="etcd.requestTimeout">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Etcd operation timeout in milliseconds</li>      </td>
      <td>10000</td>
    </tr>
  </tbody>
</table>


## `etcd.use.embed`

<table id="etcd.use.embed">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to enable embedded Etcd (an in-process EtcdServer).</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `etcd.data.dir`

<table id="etcd.data.dir">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Embedded Etcd only. please adjust in embedded Milvus: /tmp/milvus/etcdData/</li>      </td>
      <td>default.etcd</td>
    </tr>
  </tbody>
</table>


## `etcd.auth.enabled`

<table id="etcd.auth.enabled">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to enable authentication</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `etcd.auth.userName`

<table id="etcd.auth.userName">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>username for etcd authentication</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `etcd.auth.password`

<table id="etcd.auth.password">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>password for etcd authentication</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


