---
id: configure_minio.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure minio for Milvus.
---

# minio-related Configurations

Related configuration of MinIO/S3/GCS or any other service supports S3 API, which is responsible for data persistence for Milvus.

We refer to the storage service as MinIO/S3 in the following description for simplicity.

## `minio.address`

<table id="minio.address">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Address of MinIO/S3</li>      </td>
      <td>localhost</td>
    </tr>
  </tbody>
</table>


## `minio.port`

<table id="minio.port">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Port of MinIO/S3</li>      </td>
      <td>9000</td>
    </tr>
  </tbody>
</table>


## `minio.accessKeyID`

<table id="minio.accessKeyID">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>accessKeyID of MinIO/S3</li>      </td>
      <td>minioadmin</td>
    </tr>
  </tbody>
</table>


## `minio.secretAccessKey`

<table id="minio.secretAccessKey">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>MinIO/S3 encryption string</li>      </td>
      <td>minioadmin</td>
    </tr>
  </tbody>
</table>


## `minio.useSSL`

<table id="minio.useSSL">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Access to MinIO/S3 with SSL</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `minio.ssl.tlsCACert`

<table id="minio.ssl.tlsCACert">
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
      <td>/path/to/public.crt</td>
    </tr>
  </tbody>
</table>


## `minio.bucketName`

<table id="minio.bucketName">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Bucket name in MinIO/S3</li>      </td>
      <td>a-bucket</td>
    </tr>
  </tbody>
</table>


## `minio.rootPath`

<table id="minio.rootPath">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The root path where the message is stored in MinIO/S3</li>      </td>
      <td>files</td>
    </tr>
  </tbody>
</table>


## `minio.useIAM`

<table id="minio.useIAM">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether to useIAM role to access S3/GCS instead of access/secret keys</li>
        <li>For more information, refer to</li>
        <li>aws: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html</li>
        <li>gcp: https://cloud.google.com/storage/docs/access-control/iam</li>
        <li>aliyun (ack): https://www.alibabacloud.com/help/en/container-service-for-kubernetes/latest/use-rrsa-to-enforce-access-control</li>
        <li>aliyun (ecs): https://www.alibabacloud.com/help/en/elastic-compute-service/latest/attach-an-instance-ram-role</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `minio.cloudProvider`

<table id="minio.cloudProvider">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Cloud Provider of S3. Supports: "aws", "gcp", "aliyun".</li>
        <li>You can use "aws" for other cloud provider supports S3 API with signature v4, e.g.: minio</li>
        <li>You can use "gcp" for other cloud provider supports S3 API with signature v2</li>
        <li>You can use "aliyun" for other cloud provider uses virtual host style bucket</li>
        <li>When useIAM enabled, only "aws", "gcp", "aliyun" is supported for now</li>      </td>
      <td>aws</td>
    </tr>
  </tbody>
</table>


## `minio.iamEndpoint`

<table id="minio.iamEndpoint">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Custom endpoint for fetch IAM role credentials. when useIAM is true & cloudProvider is "aws".</li>
        <li>Leave it empty if you want to use AWS default endpoint</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `minio.logLevel`

<table id="minio.logLevel">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Log level for aws sdk log. Supported level:  off, fatal, error, warn, info, debug, trace</li>      </td>
      <td>fatal</td>
    </tr>
  </tbody>
</table>


## `minio.region`

<table id="minio.region">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Specify minio storage system location region</li>      </td>
      <td></td>
    </tr>
  </tbody>
</table>


## `minio.useVirtualHost`

<table id="minio.useVirtualHost">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>Whether use virtual host mode for bucket</li>      </td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `minio.requestTimeoutMs`

<table id="minio.requestTimeoutMs">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>minio timeout for request time in milliseconds</li>      </td>
      <td>10000</td>
    </tr>
  </tbody>
</table>


## `minio.listObjectsMaxKeys`

<table id="minio.listObjectsMaxKeys">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>The maximum number of objects requested per batch in minio ListObjects rpc, </li>
        <li>0 means using oss client by default, decrease these configration if ListObjects timeout</li>      </td>
      <td>0</td>
    </tr>
  </tbody>
</table>


