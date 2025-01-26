---
id: multimodal_retrieval_amazon_reviews.md
summary: In this notebook, we will build a multimodal retrieval tool for images and text. The user will specify the query as a source image and an instruction, and the closest match, according to our embedding models, will be returned from the vector database. We will improve the ranking of the retrieved results by prompting a Large Language-Vision Model (LLVM) to score them in terms of relevance to the query.
title: Multimodal Retrieval with Amazon Reviews Dataset and LLVM Reranking
---

# Multimodal Retrieval with Amazon Reviews Dataset and LLVM Reranking

In this notebook, we will build a multimodal retrieval tool for images and text. The user will specify the query as a source image and an instruction, and the closest match, according to our embedding models, will be returned from the vector database. We will improve the ranking of the retrieved results by prompting a Large Language-Vision Model (LLVM) to score them in terms of relevance to the query.

We will use the following tools:

- HuggingFace model and dataset hubs
- PyTorch for inference
- Multimodal embedding model: `visual_bge`
- Large language-vision model `phi_3_vision_mlx`
- Vector database: Zilliz Cloud Serverless


## 1. Indexing

<img src="../../../assets/indexing.png" width=1000px />


### (a) Download and unzip data

We are using a small subset of the ["Amazon Reviews 2023" dataset](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023). This dataset was originally created for performing research into training embedding models specialized for recommender systems. We will be solely using the images and ignoring other fields such as the customer reviews text.



```shell
$ wget https://github.com/milvus-io/bootcamp/releases/download/data/amazon_reviews_2023_subset.tar.gz
$ tar -xzf amazon_reviews_2023_subset.tar.gz
```

    --2024-12-12 12:08:06--  https://github.com/milvus-io/bootcamp/releases/download/data/amazon_reviews_2023_subset.tar.gz
    Resolving github.com (github.com)... 140.82.116.4
    Connecting to github.com (github.com)|140.82.116.4|:443... connected.
    HTTP request sent, awaiting response... 302 Found
    Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/201441751/18744249-982d-4438-bde7-22c2967d50cb?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20241212%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241212T200807Z&X-Amz-Expires=300&X-Amz-Signature=f51cf666a7781edf9b7b3df9e551e237751d9bd565191a0becf6bc371a3dba88&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3Damazon_reviews_2023_subset.tar.gz&response-content-type=application%2Foctet-stream [following]
    --2024-12-12 12:08:07--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/201441751/18744249-982d-4438-bde7-22c2967d50cb?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20241212%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241212T200807Z&X-Amz-Expires=300&X-Amz-Signature=f51cf666a7781edf9b7b3df9e551e237751d9bd565191a0becf6bc371a3dba88&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3Damazon_reviews_2023_subset.tar.gz&response-content-type=application%2Foctet-stream
    Resolving objects.githubusercontent.com (objects.githubusercontent.com)... 185.199.110.133, 185.199.111.133, 185.199.109.133, ...
    Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.110.133|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 20598434 (20M) [application/octet-stream]
    Saving to: ‘amazon_reviews_2023_subset.tar.gz’
    
    amazon_reviews_2023 100%[===================>]  19.64M   499KB/s    in 39s     
    
    2024-12-12 12:08:47 (512 KB/s) - ‘amazon_reviews_2023_subset.tar.gz’ saved [20598434/20598434]
    


### (b) Download and load model

We use a multimodal text-image embedding model called [Visualized BGE](https://huggingface.co/BAAI/bge-visualized) (see [Zhou et al., 2024](https://arxiv.org/abs/2406.04292) for more details). At a high-level, it works by converting the image into "visual tokens" and inputting these to the language model along with the text tokens. The model can embed text and image information into the same latent space thus enabling multimodal search.



```shell
$ wget https://huggingface.co/BAAI/bge-visualized/resolve/main/Visualized_base_en_v1.5.pth
```

    --2024-11-25 11:44:17--  https://huggingface.co/BAAI/bge-visualized/resolve/main/Visualized_base_en_v1.5.pth
    Resolving huggingface.co (huggingface.co)... 

    python(41186) MallocStackLogging: can't turn off malloc stack logging because it was not enabled.


    2600:9000:234c:5e00:17:b174:6d00:93a1, 2600:9000:234c:0:17:b174:6d00:93a1, 2600:9000:234c:b000:17:b174:6d00:93a1, ...
    Connecting to huggingface.co (huggingface.co)|2600:9000:234c:5e00:17:b174:6d00:93a1|:443... connected.
    HTTP request sent, awaiting response... 302 Found
    Location: https://cdn-lfs-us-1.hf.co/repos/00/84/008494bcd5b0797c1b2f376d3b31f3064cd16fcf8e9289e3635456afee9d710a/07e58cf70ee6962530490ef1ac5b632e7e0153ba8c7ed49d55e0f41ec97bf6a6?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27Visualized_base_en_v1.5.pth%3B+filename%3D%22Visualized_base_en_v1.5.pth%22%3B&Expires=1732823057&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTczMjgyMzA1N319LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy11cy0xLmhmLmNvL3JlcG9zLzAwLzg0LzAwODQ5NGJjZDViMDc5N2MxYjJmMzc2ZDNiMzFmMzA2NGNkMTZmY2Y4ZTkyODllMzYzNTQ1NmFmZWU5ZDcxMGEvMDdlNThjZjcwZWU2OTYyNTMwNDkwZWYxYWM1YjYzMmU3ZTAxNTNiYThjN2VkNDlkNTVlMGY0MWVjOTdiZjZhNj9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPSoifV19&Signature=PEGXgvZed6GYZZqww8eFuW38OhbEYReY3fSRdvGdZZnR23Rqv8rBjudH4MmOfPpJukLo4m47uNrePndyLr2BWZEjS-sc0judKl5gxLWXTG-66%7EOkmx5oyCoMj2t7diaf0RyMpZDTjiJdClmm6tBXiId1MJmi1--48KuMgrvXdyNIHefKEWjNzFXPisknK7crGn9VkVjGVOb6ul5TjqZEW5XYoSOIipe7xC1u%7EKJ2iw%7EyKadiqcZRfzRPf4qA9knYuuQj10xTjzOmXO6GEBxWUx0FbkUIys%7EOD%7EXkFK1OY7diXi-uP%7ElRlMrZzzlgIHS093WiZSQTyMpY7iOkQgIXYQ__&Key-Pair-Id=K24J24Z295AEI9 [following]
    --2024-11-25 11:44:17--  https://cdn-lfs-us-1.hf.co/repos/00/84/008494bcd5b0797c1b2f376d3b31f3064cd16fcf8e9289e3635456afee9d710a/07e58cf70ee6962530490ef1ac5b632e7e0153ba8c7ed49d55e0f41ec97bf6a6?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27Visualized_base_en_v1.5.pth%3B+filename%3D%22Visualized_base_en_v1.5.pth%22%3B&Expires=1732823057&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTczMjgyMzA1N319LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy11cy0xLmhmLmNvL3JlcG9zLzAwLzg0LzAwODQ5NGJjZDViMDc5N2MxYjJmMzc2ZDNiMzFmMzA2NGNkMTZmY2Y4ZTkyODllMzYzNTQ1NmFmZWU5ZDcxMGEvMDdlNThjZjcwZWU2OTYyNTMwNDkwZWYxYWM1YjYzMmU3ZTAxNTNiYThjN2VkNDlkNTVlMGY0MWVjOTdiZjZhNj9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPSoifV19&Signature=PEGXgvZed6GYZZqww8eFuW38OhbEYReY3fSRdvGdZZnR23Rqv8rBjudH4MmOfPpJukLo4m47uNrePndyLr2BWZEjS-sc0judKl5gxLWXTG-66%7EOkmx5oyCoMj2t7diaf0RyMpZDTjiJdClmm6tBXiId1MJmi1--48KuMgrvXdyNIHefKEWjNzFXPisknK7crGn9VkVjGVOb6ul5TjqZEW5XYoSOIipe7xC1u%7EKJ2iw%7EyKadiqcZRfzRPf4qA9knYuuQj10xTjzOmXO6GEBxWUx0FbkUIys%7EOD%7EXkFK1OY7diXi-uP%7ElRlMrZzzlgIHS093WiZSQTyMpY7iOkQgIXYQ__&Key-Pair-Id=K24J24Z295AEI9
    Resolving cdn-lfs-us-1.hf.co (cdn-lfs-us-1.hf.co)... 18.173.121.63, 18.173.121.3, 18.173.121.55, ...
    Connecting to cdn-lfs-us-1.hf.co (cdn-lfs-us-1.hf.co)|18.173.121.63|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 392860018 (375M) [binary/octet-stream]
    Saving to: ‘Visualized_base_en_v1.5.pth.2’
    
    Visualized_base_en_ 100%[===================>] 374.66M  40.5MB/s    in 9.3s    
    
    2024-11-25 11:44:27 (40.2 MB/s) - ‘Visualized_base_en_v1.5.pth.2’ saved [392860018/392860018]
    


We wrap the model in an `Encoder` class that has convenient utility functions for embedding `(text, img)` pairs and individual `img`'s.



```python
import torch
from visual_bge.modeling import Visualized_BGE


class Encoder:
    def __init__(self, model_name: str, model_path: str):
        self.model = Visualized_BGE(model_name_bge=model_name, model_weight=model_path)
        self.model.eval()

    def encode_query(self, image_path: str, text: str) -> list[float]:
        with torch.no_grad():
            query_emb = self.model.encode(image=image_path, text=text)
        return query_emb.tolist()[0]

    def encode_image(self, image_path: str) -> list[float]:
        with torch.no_grad():
            query_emb = self.model.encode(image=image_path)
        return query_emb.tolist()[0]


model_name = "BAAI/bge-base-en-v1.5"
model_path = "./Visualized_base_en_v1.5.pth"  # Change to your own value if using a different model path
encoder = Encoder(model_name, model_path)
```

    /opt/miniconda3/envs/milvus/lib/python3.12/site-packages/timm/models/layers/__init__.py:48: FutureWarning: Importing from timm.models.layers is deprecated, please import via timm.layers
      warnings.warn(f"Importing from {__name__} is deprecated, please import via timm.layers", FutureWarning)
    /opt/miniconda3/envs/milvus/lib/python3.12/site-packages/huggingface_hub/file_download.py:1142: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
      warnings.warn(
    /Users/stefanwebb/Code/FlagEmbedding/research/visual_bge/visual_bge/modeling.py:106: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
      self.load_state_dict(torch.load(model_weight, map_location='cpu'))
    /opt/miniconda3/envs/milvus/lib/python3.12/site-packages/huggingface_hub/file_download.py:1142: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
      warnings.warn(


### (c) Embed images

For each image in the downloaded dataset, we pass it through the embedding model to obtain the output vector. Embedding may take some time. For example, a MacBook Pro M3 embeds around nine images per second. The throughput is likely to be much higher if running on a more powerful hardware such as Nvidia GPU.


```python
import os
from tqdm import tqdm
from glob import glob
```


```python
data_dir = "./images_folder"
image_list = glob(os.path.join(data_dir, "images", "*.jpg"))
```


```python
# Loop over images in dataset and produce embeddings
image_dict = {}
for image_path in tqdm(image_list, desc="Generating image embeddings: "):
    try:
        image_dict[image_path] = encoder.encode_image(image_path)

    except Exception as e:
        print(f"Failed to generate embedding for {image_path}. Skipped.")
        continue
```

    Generating image embeddings: 100%|██████████| 900/900 [01:45<00:00,  8.54it/s]


### (d) Store embeddings in vector database
In order to perform efficient similarity search over embeddings, we need to store them in a [vector database](https://zilliz.com/learn/introduction-to-unstructured-data). In this demo, we use Milvus Lite, a lightweight version of a popular open-source vector database [Milvus](https://milvus.io/).

By specifying uri to a file path, it persists all data to a local file:


```python
from pymilvus import MilvusClient

# Connect to Milvus client given URI
milvus_client = MilvusClient(uri="multimodal_demo.db")
```

Then, we create a "collection" in our database, which is akin to a table in relational databases.

We need to specify the dimension of our embeddings, and will use a dynamic schema rather than specifying the fields and their data types beforehand.



```python
from pymilvus import FieldSchema, DataType, CollectionSchema

dim = 768
collection_name = "amazon_reviews_2023"

schema = CollectionSchema(
    [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="image_path", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
    ]
)

if milvus_client.has_collection(collection_name=collection_name):
    milvus_client.drop_collection(collection_name=collection_name)

milvus_client.create_collection(
    collection_name,
    dim,
    primary_field_name="id",
    vector_field_name="vector",
    metric_type="COSINE",
    auto_id=True,
    schema=schema,
)

print(milvus_client.list_collections())
```

    ['amazon_reviews_2023']


Finally, we insert our data into the database. Each entity - like a row in a relational database - will be a pair of image path and embedding. Since we use auto id, we can omit the id field.


```python
# NOTE: Don't run this cell more than once or duplicate entries will be inserted!
milvus_client.insert(
    collection_name=collection_name,
    data=[{"image_path": k, "vector": v} for k, v in image_dict.items()],
)
```

Now, all the data is ingested into Milvus vector database. We are ready for multi-modal search!

## 2. Retrieval

<img src="../../../assets/retrieval.png" width=1000px />


After constructing the index of our dataset, a user comes along and would like to perform a search query. In this example, the query will be multimodal in that it contains both a text instruction and a source image.



```python
query_image = os.path.join(data_dir, "leopard.jpg")
query_text = "phone case with this image theme"
```

We embed the query `(text, img)` pair with the same model used to embed the targets, and perform a similarity search in our vector database returning the top 9 results.



```python
# Generate query embedding given image and text instructions
query_vec = encoder.encode_query(image_path=query_image, text=query_text)

search_results = milvus_client.search(
    collection_name=collection_name,
    data=[query_vec],
    output_fields=["image_path"],
    limit=9,  # Max number of search results to return
    search_params={"metric_type": "COSINE", "params": {}},  # Search parameters
)[0]

retrieved_images = [hit.get("entity").get("image_path") for hit in search_results]
print(retrieved_images)
```

    ['./images_folder/images/518Gj1WQ-RL._AC_.jpg', './images_folder/images/41n00AOfWhL._AC_.jpg', './images_folder/images/51Wqge9HySL._AC_.jpg', './images_folder/images/51R2SZiywnL._AC_.jpg', './images_folder/images/516PebbMAcL._AC_.jpg', './images_folder/images/51RrgfYKUfL._AC_.jpg', './images_folder/images/515DzQVKKwL._AC_.jpg', './images_folder/images/51BsgVw6RhL._AC_.jpg', './images_folder/images/51INtcXu9FL._AC_.jpg']


To make the results easy to understand for us and efficient for the reranker step, we combine the query and retrieved images into a single one.



```python
import numpy as np
import cv2

img_height = 300
img_width = 300
row_count = 3


def create_panoramic_view(query_image_path: str, retrieved_images: list) -> np.ndarray:
    """
    creates a 5x5 panoramic view image from a list of images

    args:
        images: list of images to be combined

    returns:
        np.ndarray: the panoramic view image
    """
    panoramic_width = img_width * row_count
    panoramic_height = img_height * row_count
    panoramic_image = np.full(
        (panoramic_height, panoramic_width, 3), 255, dtype=np.uint8
    )

    # create and resize the query image with a blue border
    query_image_null = np.full((panoramic_height, img_width, 3), 255, dtype=np.uint8)
    query_image = Image.open(query_image_path).convert("RGB")
    query_array = np.array(query_image)[:, :, ::-1]
    resized_image = cv2.resize(query_array, (img_width, img_height))

    border_size = 10
    blue = (255, 0, 0)  # blue color in BGR
    bordered_query_image = cv2.copyMakeBorder(
        resized_image,
        border_size,
        border_size,
        border_size,
        border_size,
        cv2.BORDER_CONSTANT,
        value=blue,
    )

    query_image_null[img_height * 2 : img_height * 3, 0:img_width] = cv2.resize(
        bordered_query_image, (img_width, img_height)
    )

    # add text "query" below the query image
    text = "query"
    font_scale = 1
    font_thickness = 2
    text_org = (10, img_height * 3 + 30)
    cv2.putText(
        query_image_null,
        text,
        text_org,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        blue,
        font_thickness,
        cv2.LINE_AA,
    )

    # combine the rest of the images into the panoramic view
    retrieved_imgs = [
        np.array(Image.open(img).convert("RGB"))[:, :, ::-1] for img in retrieved_images
    ]
    for i, image in enumerate(retrieved_imgs):
        image = cv2.resize(image, (img_width - 4, img_height - 4))
        row = i // row_count
        col = i % row_count
        start_row = row * img_height
        start_col = col * img_width

        border_size = 2
        bordered_image = cv2.copyMakeBorder(
            image,
            border_size,
            border_size,
            border_size,
            border_size,
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0),
        )
        panoramic_image[
            start_row : start_row + img_height, start_col : start_col + img_width
        ] = bordered_image

        # add red index numbers to each image
        text = str(i + 1)
        org = (start_col + 50, start_row + 30)
        (font_width, font_height), baseline = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2
        )

        top_left = (org[0] - 48, start_row + 2)
        bottom_right = (org[0] - 48 + font_width + 5, org[1] + baseline + 5)

        cv2.rectangle(
            panoramic_image, top_left, bottom_right, (255, 255, 255), cv2.FILLED
        )
        cv2.putText(
            panoramic_image,
            text,
            (start_col + 10, start_row + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

    # combine the query image with the panoramic view
    panoramic_image = np.hstack([query_image_null, panoramic_image])
    return panoramic_image
```


```python
from PIL import Image
from IPython.display import display
import os

combined_image_path = os.path.join(data_dir, "combined_image.jpg")
panoramic_image = create_panoramic_view(query_image, retrieved_images)
cv2.imwrite(combined_image_path, panoramic_image)

combined_image = Image.open(combined_image_path)
display(combined_image.resize((512, 512)))
```


    
![png](../../../assets/multimodal_retrieval_amazon_reviews_files/multimodal_retrieval_amazon_reviews_27_0.png)
    


We see the query image is in the lower left with a blue border, and the search results are numbered from 1 to 9 with 1 being the closest one in the vector space. Image 7 seems like a good match for the query.


## 3. Reranking

<img src="../../../assets/generation.png" width=1000px />

We can improve upon the raw retrieval results by reranking them with a separate model. We use a Large Language-Vision Model (LLVM) for this purpose, and perform the reranking with a prompt.

We use a particular library, `phi_3_vision_mlx`, for the LLVM that is designed to run efficiently on Macs. If you have access to a Nvidia card or other such GPU hardware, the LLVM can be loaded directly with HuggingFace's `Transformers` library.

Our LLVM is run locally. **Another option is to use a service such as Amazon Bedrock to run, for example, Llama 3.2 11B in the cloud.**



```python
from phi_3_vision_mlx import generate

# The model will be downloaded the first time `generate` is called and cached locally
```

The reranker is more effective if we pass a description of the query image in addition to the image itself. We use the LLVM for generating this caption as well.



```python
prompt = "You are a helpful assistant that captions images with short, descriptive, informative text no longer than a sentence. Caption this image."

query_caption = generate(prompt=prompt, images=query_image)
query_caption = query_caption.removesuffix("<|end|>")
```

    *** Prompt ***
    <|user|>
    <|image_1|>
    You are a helpful assistant that captions images with short, descriptive, informative text no longer than a sentence. Caption this image.<|end|>
    <|assistant|>
    *** Images ***
    <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=640x480 at 0x38C144620>
    *** Output ***
    The image shows a close-up of a leopard's face with a focus on its spotted fur and green eyes.<|end|> 
    
    
    Prompt: 72.85 tokens-per-sec (1961 tokens / 26.9 sec)
    Generate: 7.03 tokens-per-sec (28 tokens / 3.8 sec)



```python
query_caption
```




    "The image shows a close-up of a leopard's face with a focus on its spotted fur and green eyes."



Now, we construct the reranking prompt including both the query instruction and a textual description of the query image.



```python
information = (
    "You are responsible for ranking results for a Composed Image Retrieval. "
    "The user retrieves an image with an 'instruction' indicating their retrieval intent. "
    "For example, if the user queries a red car with the instruction 'change this car to blue,' a similar type of car in blue would be ranked higher in the results. "
    "Now you would receive instruction and an image containing the query image and multiple result images. The query image has a blue border and relates to the text instruction, and the result images have a red index number in their top left. Do not misunderstand it!"
    f"User instruction: {query_text} \n\n"
    f"Caption of query image: {query_caption} \n\n"
    "Provide a new ranked list of indices from most suitable to least suitable, followed by an explanation for the top 1 most suitable item only."
    "The format of the response has to be 'Ranked list: []' with the indices in brackets as integers, followed by 'Reasons:' plus the explanation why this most fit user's query intent."
)
```

We call the LLVM with this prompt, also passing composite image of the query and retrieved images. For efficiency, we combine the images into a single one that is scaled down, although you could also pass the images separately.



```python
generate(prompt=information, images=combined_image_path)
```

    *** Prompt ***
    <|user|>
    <|image_1|>
    You are responsible for ranking results for a Composed Image Retrieval. The user retrieves an image with an 'instruction' indicating their retrieval intent. For example, if the user queries a red car with the instruction 'change this car to blue,' a similar type of car in blue would be ranked higher in the results. Now you would receive instruction and an image containing the query image and multiple result images. The query image has a blue border and relates to the text instruction, and the result images have a red index number in their top left. Do not misunderstand it!User instruction: phone case with this image theme 
    
    Caption of query image: The image shows a close-up of a leopard's face with a focus on its spotted fur and green eyes. 
    
    Provide a new ranked list of indices from most suitable to least suitable, followed by an explanation for the top 1 most suitable item only.The format of the response has to be 'Ranked list: []' with the indices in brackets as integers, followed by 'Reasons:' plus the explanation why this most fit user's query intent.<|end|>
    <|assistant|>
    *** Images ***
    <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1200x900 at 0x38C16D8E0>
    *** Output ***
    Ranked list: [7, 8, 5, 3, 2, 4, 1, 6]
    
    Reasons: The most suitable item is the one with the leopard theme, which matches the user's query instruction for a phone case with a similar theme.<|end|> 
    
    
    Prompt: 149.19 tokens-per-sec (2172 tokens / 14.6 sec)
    Generate: 9.32 tokens-per-sec (65 tokens / 6.9 sec)





    "Ranked list: [7, 8, 5, 3, 2, 4, 1, 6]\n\nReasons: The most suitable item is the one with the leopard theme, which matches the user's query instruction for a phone case with a similar theme.<|end|>"



Visualizing the query and retrieved images again after the reranking:



```python
# Hardcoding results, but could use constrained sampling / post-processing to retrieve
reranked_retrieved_images = [retrieved_images[i - 1] for i in [7, 8, 5, 3, 2, 4, 1, 6]]

reranked_combined_image_path = os.path.join(data_dir, "reranked_combined_image.jpg")
panoramic_image = create_panoramic_view(query_image, reranked_retrieved_images)
cv2.imwrite(reranked_combined_image_path, panoramic_image)

reranked_combined_image = Image.open(reranked_combined_image_path)
display(reranked_combined_image.resize((512, 512)))
```


    
![png](../../../assets/multimodal_retrieval_amazon_reviews_files/multimodal_retrieval_amazon_reviews_39_0.png)
    


The reranker has successfully chosen (the previous) image 7 as the top match for the query and gives a sensible reason. A weird artifact is that the LLVM only ranked the top 8 images and dropped the last one.


## Summary

- Demonstration of building a multimodal image search with Milvus Lite
- Open-source tools were used for the data and modelling components
- Same method scales to 100s of billions of images by parallelizing calculating embedding and changing the Milvus deployment.
- Rather than tackle the complexities of self-hosting, you can use [Zilliz Cloud](https://zilliz.com/cloud) for which we take care of deployment.


### Go to https://milvus.io/bootcamp for more content on awesome vector database applications!

