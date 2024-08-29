---
id: embed-with-mgte.md
order: 9
summary: mGTE is is the latest in the GTE (General Text Embedding) family of models.
title: mGTE
---

# mGTE

[mGTE](https://arxiv.org/pdf/2407.19669) is the latest in the GTE (General Text Embedding) family of models, featuring several key attributes:

- __High Performance__: Achieves state-of-the-art (SOTA) results in multilingual retrieval tasks and multi-task representation model evaluations when compared to models of similar size.
- __Training Architecture__: Trained using an encoder-only transformers architecture, resulting in a smaller model size. Unlike previous models based on decode-only LLM architecture (e.g., gte-qwen2-1.5b-instruct), this model has lower hardware requirements for inference, offering a 10x increase in inference speed.
- __Long Context__: Supports text lengths up to __8192__ tokens.
- __Multilingual Capability__: Supports over __70__ languages.
- __Elastic Dense Embedding__: Support elastic output dense representation while maintaining the effectiveness of downstream tasks, which significantly reduces storage costs and improves execution efficiency.
- __Sparse Vectors__: In addition to dense representations, it can also generate sparse vectors.

Milvus integrates with the mGTE model using the __MGTEEmbeddingFunction__ class. This class handles the computation of embeddings and returns them in a format compatible with Milvus for indexing and searching.

To use this feature, install the necessary dependencies:

```bash
pip install --upgrade pymilvus
pip install "pymilvus[model]"
```

Then, instantiate the __MGTEEmbeddingFunction__:

```python
from pymilvus.model.hybrid import MGTEEmbeddingFunction

mgte_ef = MGTEEmbeddingFunction(
    model_name='Alibaba-NLP/gte-multilingual-base', # Specify the model name
    device='cpu', # Specify the device to use, e.g., 'cpu' or 'cuda:0'
    use_fp16=False # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
)
```

__Parameters__:

- __model_name__ (_string_)

    The name of the model to use for encoding. The value defaults to __Alibaba-NLP/gte-multilingual-base__.

- __device__ (_string_)

    The device to use, with __cpu__ for the CPU and __cuda:n__ for the nth GPU device.

- __use_fp16__ (_bool_)

    Whether to utilize 16-bit floating-point precision (fp16). Specify __False__ when __device__ is __cpu__.

To create embeddings for documents, use the __encode_documents()__ method:

```python
docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
]

docs_embeddings = mgte_ef.encode_documents(docs)

# Print embeddings
print("Embeddings:", docs_embeddings)
# Print dimension of dense embeddings
print("Dense document dim:", mgte_ef.dim["dense"], docs_embeddings["dense"][0].shape)
# Since the sparse embeddings are in a 2D csr_array format, we convert them to a list for easier manipulation.
print("Sparse document dim:", mgte_ef.dim["sparse"], list(docs_embeddings["sparse"])[0].shape)
```

The expected output is similar to the following:

```python
Embeddings: {'dense': [tensor([-4.9148e-03,  1.6553e-02, -9.5524e-03, ..., -7.9425e-03, 
        -6.7889e-02, -2.5080e-02]), tensor([ 3.0364e-03, -6.6951e-04,  2.5661e-03, ..., 4.9563e-02, 
        -2.6081e-02,  1.1404e-03]), tensor([ -2.5712e-02,  9.3124e-02,  2.8404e-02, ..., 6.0707e-02, 
        -2.0558e-02, -4.2050e-02])], 'sparse': <3x250002 sparse array of type '<class 'numpy.float64'>'
    with 41 stored elements in Compressed Sparse Row format>}
Dense document dim: 768 torch.Size([768])
Sparse document dim: 250002 (1, 250002)
```

To create embeddings for queries, use the __encode_queries()__ method:

```python
queries = ["When was artificial intelligence founded", 
           "Where was Alan Turing born?"]

query_embeddings = mgte_ef.encode_queries(queries)

# Print embeddings
print("Embeddings:", query_embeddings)
# Print dimension of dense embeddings
print("Dense query dim:", mgte_ef.dim["dense"], query_embeddings["dense"][0].shape)
# Since the sparse embeddings are in a 2D csr_array format, we convert them to a list for easier manipulation.
print("Sparse query dim:", mgte_ef.dim["sparse"], list(query_embeddings["sparse"])[0].shape)
```

The expected output is similar to the following:

```python
Embeddings: {'dense': [tensor([6.5884e-03, -7.9415e-03, -3.3669e-02, ...,  1.4615e-02, 
        -8.0653e-02, -3.4105e-03]), tensor([ 2.9341e-02,  6.0349e-02,  2.7232e-02, ..., 7.9408e-02, 
        8.2720e-03, -2.3458e-02])], 'sparse': <2x250002 sparse array of type '<class 'numpy.float64'>'
    with 13 stored elements in Compressed Sparse Row format>}
Dense query dim: 768 torch.Size([768])
Sparse query dim: 250002 (1, 250002)
```
