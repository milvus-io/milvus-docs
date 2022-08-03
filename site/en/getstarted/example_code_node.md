---
id: example_code_node.md
label: Node.js
order: 1
group: example_code.md
summary: Get started with Milvus faster using this Node.js example code.
---

{{tab}}

# Run Milvus using Node.js

This topic describes how to run Milvus using Node.js.


## 1.  Initialize a Node.js Project
```bash
npm init
```  

<div class="alert note">
Node.js version 12 or later is required. View <a href="https://www.cloudbees.com/blog/node-js-tutorial">Node.js Beginners Guide</a> for information about installing the correct version for your system.
</div>



## 2.  Install TypeScript and Node Milvus SDK and its dependencies

```bash
npm install @zilliz/milvus2-sdk-node typescript --save
```


## 3. Download sample code HelloMilvus.ts
```bash
$ wget https://raw.githubusercontent.com/milvus-io/milvus-sdk-node/main/example/HelloMilvus.ts
```

## 4. Scan HelloMilvus.ts

This sample code does the following:

- Imports the Node.js SDK package:
```ts
import { MilvusClient } from "@zilliz/milvus2-sdk-node"
import { DataType } from "@zilliz/milvus2-sdk-node/dist/milvus/types/Common";
import { InsertReq } from "@zilliz/milvus2-sdk-node/dist/milvus/types/Insert";
```

- Connects to the Milvus server:
```ts
const milvusClient = new MilvusClient("localhost:19530");
const collectionManager = milvusClient.collectionManager;
```

- Creates a collection:
```ts
const collectionName = "hello_milvus";
    const dim = "4";
    const createRes = await collectionManager.createCollection(
        {
            collection_name: collectionName,
            fields: [
                {
                    name: "count",
                    data_type: DataType.VarChar,
                    is_primary_key: true,
                    type_params: {
                      max_length: '100',
                    },
                }, 
                {
                    name: "random_value",
                    data_type: DataType.Double,
                    description: "",
                }, 
                {
                    name: "float_vector",
                    data_type: DataType.FloatVector,
                    description: "",
                    type_params: {
                      dim
                    }
                }
            ]
          }
    );


    console.log("--- Create collection ---", createRes, collectionName);
```


- Inserts vectors in the new collection:
```ts
const generateInsertData = function generateInsertData(
  fields: { isVector: boolean; dim?: number; name: string; isBool?: boolean }[],
  count: number) {
    const results = [];
    while (count > 0) {
      let value: any = {};
  
      fields.forEach((v) => {
        const { isVector, dim, name, isBool } = v;
        value[name] = isVector
          ? [...Array(dim)].map(() => Math.random() * 10)
          : isBool
          ? count % 2 === 0
          : count;
      });

      value["count"] = count;
      results.push(value);
      count--;
    }
    return results;
}

    const fields = [
      {
        isVector: true,
        dim: 4,
        name: "float_vector",
      },
      {
        isVector: false,
        name: "random_value",
      },
    ];
    const vectorsData = generateInsertData(fields, 1000);
  
    const params: InsertReq = {
      collection_name: collectionName,
      fields_data: vectorsData,
      partition_name: "test",
    };
  
    await milvusClient.dataManager.insert(params);
    console.log("--- Insert Data to Collection ---");
```

- Loads the collection and builds index on it:
``` ts
    await milvusClient.indexManager.createIndex({
      collection_name: collectionName,
      field_name: "float_vector",
      extra_params: {
        index_type: "IVF_FLAT",
        metric_type: "L2",
        params: JSON.stringify({ nlist: 10 }),
      },
    });
    console.log("--- Create Index in Collection ---");
```

- Searches the collection:
```ts
        // need load collection before search
    const loadCollectionRes = await collectionManager.loadCollectionSync({
      collection_name: collectionName,
    });
    console.log("--- Load collection (" + collectionName + ") ---", loadCollectionRes);


    const result = await milvusClient.dataManager.search({
      collection_name: collectionName,
      vectors: [vectorsData[0]["float_vector"]],
      search_params: {
        anns_field: "float_vector",
        topk: "4",
        metric_type: "L2",
        params: JSON.stringify({ nprobe: 1024 }),
        round_decimal: 4,
      },
      output_fields: ["count"],
      vector_type: DataType.FloatVector,
    });

    console.log("--- Search collection (" + collectionName + ") ---", result);
```

- Releases the collection:
```ts
    const releaseRes = await collectionManager.releaseCollection({
      collection_name: collectionName,
    });
    console.log("--- Release Collection ---", releaseRes);
``` 

- Drops the collection:
```tw
    const dropRes = await collectionManager.dropCollection({
      collection_name: collectionName,
    });
    console.log("--- Drop Collection ---", dropRes);
```

## 5. Compile the file
```bash
tsc MilvusHello.ts
```


## 6. Run the example
```bash
node MilvusHello.ts
```


<br/>


*Congratulations! You have successfully booted Milvus Standalone and created your first collection.*
