

# Run Milvus using **NodeJS**

This topic describes how to run Milvus using NodeJS.


1.  Initialize NodeJS Project
```bash
   npm init
```  

<div class="alert note">
Node version 12 or higher is required. View <a href="https://www.cloudbees.com/blog/node-js-tutorial">NodeJS Beginners Guide</a> for information about installing the correct version for your system.
</div>



2.  Install TypeScript and Node Milvus SDK and its dependencies:
```bash
   npm install @zilliz/milvus2-sdk-node typescript --save
```


3. Download sample code **hello_milvus.py**:

```bash
$ wget https://raw.githubusercontent.com/milvus-io/milvus-sdk-node/main/example/MilvusHello.ts
```

4. Scan hello_milvus.py. This sample code does the following:
- Imports the PyMilvus package:
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
                    data_type: DataType.Int64,
                    is_primary_key: true,
                    description: "",
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

- Creates a partition in the collection:
```ts
    await milvusClient.partitionManager.createPartition({
      collection_name: collectionName,
      partition_name: "test",
    });

    console.log("--- Create Partition in Collection ---", collectionName, "test");
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

...
...

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

- Queries the collection
```ts
    const queryRes = await milvusClient.dataManager.query({
      collection_name: collectionName,
      expr: "count < 10",
      output_fields: ["count", "random_value", "float_vector"]
    });
    console.log("--- Query Collection ---", queryRes);
```

- Releases the collection
```ts
    const releaseRes = await collectionManager.releaseCollection({
      collection_name: collectionName,
    });
    console.log("--- Release Collection ---", releaseRes);
``` 

- Drops the collection
```
    const dropRes = await collectionManager.dropCollection({
      collection_name: collectionName,
    });
    console.log("--- Drop Collection ---", dropRes);
```

5. Compile the file
```bash
    tsc MilvusHello.ts
```


6. Run the example
```bash
    node MilvusHello.ts
```


<br/>


*Congratulations! You have successfully booted Milvus Standalone and created your first collection.*
