The `vendure-plugin-milvus` plugin provides powerful integration between [Milvus](https://milvus.io/), an open-source vector database built for scalable similarity search, and [Vendure](https://www.vendure.io/), a headless commerce framework. This plugin enables seamless management of Milvus collections, partitions, aliases, users, roles, databases, indexes, vectors, and data import directly from the Vendure admin interface.

## Setup

The easiest way to set up a Milvus server is using the official docker image. You can run the following command to start a Milvus server:

```bash
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh

bash standalone_embed.sh start
```
https://milvus.io/docs/install_standalone-docker.md

## Features

- **Milvus Collection Management**: Create, update, list, describe, and delete collections.
- **Partition Management**: Create, drop, list, load, and release partitions within collections.
- **Alias Management**: Create, describe, drop, and alter aliases for collections.
- **Database Management**: Create, describe, and list Milvus databases.
- **Index Management**: Create, describe, list, and drop indexes on collections.
- **User and Role Management**: Create, describe, list, update, and delete users and roles.
- **Vector Management**: Insert, upsert, query, search, and delete vectors in collections.
- **Import Management**: Create and manage import jobs for bulk data import.

## Installation

To use this plugin, you need to have a running instance of Milvus. You can follow the [Milvus installation guide](https://milvus.io/docs/install_standalone-docker.md) for setting it up.

Install the plugin by running the following command:

```bash
npm install vendure-plugin-milvus
```
## Usage

To add the Milvus plugin to your Vendure server, import and register the plugin in your Vendure configuration file:

```ts
import { MilvusPlugin } from 'vendure-plugin-milvus';

export const config: VendureConfig = {
  // ... other configuration options
  plugins: [
    // ... other plugins
    MilvusPlugin,
  ],
};
```

## GraphQL API

The `vendure-plugin-milvus` exposes several GraphQL queries and mutations to interact with Milvus. Below is a summary of the available operations:

### Collection Management

#### Queries

- `milvusListCollections`
- `milvusDescribeCollection`
- `milvusHasCollection`
- `milvusGetCollectionStatistics`
- `milvusGetCollectionLoadState`

#### Mutations

- `milvusCreateCollection`
- `milvusDropCollection`
- `milvusRenameCollection`
- `milvusLoadCollection`
- `milvusReleaseCollection`

### Partition Management

#### Queries

- `milvusListPartitions`
- `milvusHasPartition`
- `milvusGetPartitionStatistics`

#### Mutations

- `milvusCreatePartition`
- `milvusDropPartition`
- `milvusLoadPartitions`
- `milvusReleasePartitions`

### Alias Management

#### Queries

- `milvusListAliases`
- `milvusDescribeAlias`

#### Mutations

- `milvusCreateAlias`
- `milvusDropAlias`
- `milvusAlterAlias`

### Database Management

#### Queries

- `milvusListDatabases`
- `milvusDescribeDatabase`

#### Mutations

- `milvusCreateDatabase`
- `milvusDropDatabase`

### Index Management

#### Queries

- `milvusDescribeIndex`
- `milvusListIndexes`

#### Mutations

- `milvusCreateIndex`
- `milvusDropIndex`

### User and Role Management

#### Queries

- `milvusDescribeUser`
- `milvusListUsers`
- `milvusDescribeRole`
- `milvusListRoles`

#### Mutations

- `milvusCreateUser`
- `milvusDropUser`
- `milvusUpdateUserPassword`
- `milvusGrantRoleToUser`
- `milvusRevokeRoleFromUser`
- `milvusCreateRole`
- `milvusDropRole`
- `milvusGrantPrivilegeToRole`
- `milvusRevokePrivilegeFromRole`

### Vector Management

#### Queries

- `milvusGetVector`
- `milvusQueryVector`
- `milvusSearchVector`

#### Mutations

- `milvusInsertVector`
- `milvusUpsertVector`
- `milvusDeleteVector`

### Import Management

#### Queries

- `milvusListImportJobs`
- `milvusGetImportJobProgress`

#### Mutations

- `milvusCreateImportJob`

## Examples

Here are some example GraphQL queries and mutations to get you started with the `vendure-plugin-milvus`.

### Create a Milvus Database

```graphql
mutation {
  createMilvusDatabase(input: { name: "zikzakzikzakwtf" }) {
    error_code
    reason
    code
  }
}
```

### List Collections

```graphql
{
  milvusListCollections(params: {
    dbName: "zikzakzikzakwtf"
  }) {
    data
    message
  }
}
```

### Create a Collection

```graphql
mutation {
  milvusCreateCollection(
    data: {
      collectionName: "zikzaks",
      dbName: "zikzakzikzakwtf",
      schema: {
        autoID: false,
        enabledDynamicField: true,
        fields: [
          { fieldName: "id", dataType: "Int64", isPrimary: true },
          {
            fieldName: "barcode",
            dataType: "Int64",
            elementTypeParams: { max_length: 13 }
          },
          {
            fieldName: "name",
            dataType: "VarChar",
            elementTypeParams: { max_length: 256 }
          },
          {
            fieldName: "channel",
            dataType: "VarChar",
            elementTypeParams: { max_length: 32 }
          },
          {
            fieldName: "userId",
            dataType: "VarChar",
            elementTypeParams: { max_length: 64 }
          },
          {
            fieldName: "vector",
            dataType: "FloatVector",
            elementTypeParams: { dim: 768 }
          }
        ]
      },
      indexParams: {
        metricType: "L2"
        indexName: "zikzakIndex"
        fieldName: "vector"
        params: { index_type: "IVF_FLAT", nlist: 1024 }
      }
    }
  ) {
    data
    message
    code
  }
}
```

### Drop a Collection

```graphql
mutation {
  milvusDropCollection(data: {
    dbName: "zikzakzikzakwtf",
    collectionName: "zikzaks"
  }) {
    data
    code
    message
  }
}
```

### List Indexes

```graphql
{
  milvusListIndexes(
    params: { dbName: "zikzakzikzakwtf", collectionName: "zikzaks" }
  ) {
    data
    code
    message
  }
}
```

### Create an Index

```graphql
mutation {
  milvusCreateIndex(
    data: {
      dbName: "zikzakzikzakwtf",
      collectionName: "zikzaks",
      indexParams: {
        metricType: "L2",
        indexName: "zikzakIndex2",
        fieldName: "barcode",
        params: { index_type: "AUTOINDEX" }
      }
    }
  ) {
    code
    data
    message
  }
}
```

### Drop an Index

```graphql
mutation {
  milvusDropIndex(
    data: {
      dbName: "zikzakzikzakwtf",
      collectionName: "zikzaks",
      indexName: "zikzakIndex2"
    }
  ) {
    data
    message
    code
  }
}
```

### Release a Collection

```graphql
mutation {
  milvusReleaseCollection(
    data: { dbName: "zikzakzikzakwtf", collectionName: "zikzaks" }
  ) {
    data
    message
    code
  }
}
```

### Load a Collection

```graphql
mutation {
  milvusLoadCollection(
    data: { dbName: "zikzakzikzakwtf", collectionName: "zikzaks" }
  ) {
    code
    message
    data
  }
}
```

### Describe a User

```graphql
{
  milvusDescribeUser(params: {
    userName: "arrrrny"
  }) {
    data
    code
    message
  }
}
```
## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/arrrrny/vendure-plugin-milvus).
