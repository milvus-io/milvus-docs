---
id: example_code_node.md
title: 通过 Node.js 使用 Milvus
label: Node.js
order: 1
group: example
summary: 使用此 Node.js 示例代码更快地开始使用 Milvus。
---

{{tab}}

# 通过 Node.js 使用 Milvus

成功启动 Milvus 服务端后，通过 Node.js 示例代码使用 Milvus。

## 1. 初始化 Node.js 项目
```bash
   npm init
```  

<div class="alert note">
需要 Node.js 版本 12 或更高版本。看法 <a href="https://www.cloudbees.com/blog/node-js-tutorial">Node.js 初学者指南</a> 有关为您的系统安装正确版本的信息。
</div>


## 2. 安装 TypeScript 和 Node Milvus SDK 及其依赖
```bash
   npm install @zilliz/milvus2-sdk-node typescript --save
```


## 3. 下载示例代码 HelloMilvus.ts
```bash
$ wget https://raw.githubusercontent.com/milvus-io/milvus-sdk-node/main/example/HelloMilvus.ts
```

## 4. 扫描 HelloMilvus.ts

此示例代码执行以下操作：

- 导入 Node.js SDK 包：
```ts
import { MilvusClient } from "@zilliz/milvus2-sdk-node"
import { DataType } from "@zilliz/milvus2-sdk-node/dist/milvus/types/Common";
import { InsertReq } from "@zilliz/milvus2-sdk-node/dist/milvus/types/Insert";
```

- 连接 Milvus 服务器：
```ts
const milvusClient = new MilvusClient("localhost:19530");
const collectionManager = milvusClient.collectionManager;
```

- 创建一个集合：
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


- 在新集合中插入向量：
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

- 加载集合并在其上构建索引：
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

- 搜索集合：
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

- 发布集合：
```ts
    const releaseRes = await collectionManager.releaseCollection({
      collection_name: collectionName,
    });
    console.log("--- Release Collection ---", releaseRes);
``` 

- 掉落集合：
```tw
    const dropRes = await collectionManager.dropCollection({
      collection_name: collectionName,
    });
    console.log("--- Drop Collection ---", dropRes);
```

## 5. 编译文件
```bash
    tsc MilvusHello.ts
```


## 6. 运行示例
```bash
    node MilvusHello.ts
```


<br/>


*恭喜！您已成功启动 Milvus Standalone 并创建了您的第一个合集。*
