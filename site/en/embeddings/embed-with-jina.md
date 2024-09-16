---
id: embed-with-jina.md
order: 8
summary: This article describes how to use the JinaEmbeddingFunction to encode documents and queries using the Jina AI embedding model.
title: Jina AI - Embed
---

# Jina AI

Jina AI's embedding models are high-performance text embedding models that can translate textual inputs into numerical representations, capturing the semantics of the text. These models excel in applications like dense retrieval, semantic textual similarity, and multilingual understanding.

Milvus integrates with Jina AI's embedding models via the `JinaEmbeddingFunction` class. This class provides methods for encoding documents and queries using the Jina AI embedding models and returning the embeddings as dense vectors compatible with Milvus indexing. To utilize this functionality, obtain an API key from [Jina AI](https://jina.ai/embeddings/).

To use this feature, install the necessary dependencies:

```bash
pip install --upgrade pymilvus
pip install "pymilvus[model]"
```

Then, instantiate the `JinaEmbeddingFunction`:

```python
from pymilvus.model.dense import JinaEmbeddingFunction

jina_ef = JinaEmbeddingFunction(
    model_name="jina-embeddings-v3", # Defaults to `jina-embeddings-v3`
    api_key=JINAAI_API_KEY, # Provide your Jina AI API key
    task="retrieval.passage",
    dimensions=1024, # Defaults to 1024
)
```

__Parameters__:

- `model_name` (*string*)
  
  The name of the Jina AI embedding model to use for encoding. You can specify any of the available Jina AI embedding model names, for example, `jina-embeddings-v2-base-en`, `jina-embeddings-v2-small-en`, etc. If you leave this parameter unspecified, `jina-embeddings-v2-base-en` will be used. For a list of available models, refer to [Jina Embeddings](https://jina.ai/embeddings).

- `api_key` (*string*)
  
  The API key for accessing the Jina AI API.

- `task` (*string*)

  The type of input passed to the model. Required for embedding models v3 and higher.

  - `"retrieval.passage"`: Used to encode large documents in retrieval tasks at indexing time.
  - `"retrieval.query"`: Used to encode user queries or questions in retrieval tasks.
  - `"classification"`: Used to encode text for text classification tasks.
  - `"text-matching"`: Used to encode text for similarity matching, such as measuring similarity between two sentences.
  - `"clustering"`: Used for clustering or reranking tasks.

- `dimensions` (*int*)

  The number of dimensions the resulting output embeddings should have. Defaults to 1024. Only supported for embedding models v3 and higher. 

To create embeddings for documents, use the `encode_documents()` method:

```python
docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
]

docs_embeddings = jina_ef.encode_documents(docs)

# Print embeddings
print("Embeddings:", docs_embeddings)
# Print dimension and shape of embeddings
print("Dim:", jina_ef.dim, docs_embeddings[0].shape)
```

The expected output is similar to the following:

```python
Embeddings: [array([9.80653837e-02, -8.54787454e-02,  7.40123838e-02,  1.35843819e-02,
       -2.19967533e-02,  1.33830833e-03, -3.48760746e-02, -3.10385060e-02,
       -3.29966731e-02,  4.74663125e-03,  3.71544659e-02,  3.54884677e-02,
        8.19305144e-03,  5.87815717e-02, -6.96594734e-03, -1.80472117e-02,
...
        2.46419664e-02,  3.45800668e-02, -1.69200692e-02, -9.93125699e-03,
       -2.75502075e-03, -8.65739491e-03, -1.19673612e-03,  6.19480573e-03,
       -1.12194521e-02, -3.99678349e-02,  3.19652334e-02, -1.26290624e-03])]
Dim: 1024 (1024,)
```

To create embeddings for queries, use the `encode_queries()` method:

```python
queries = ["When was artificial intelligence founded", 
           "Where was Alan Turing born?"]

query_embeddings = jina_ef.encode_queries(queries)

print("Embeddings:", query_embeddings)
print("Dim", jina_ef.dim, query_embeddings[0].shape)
```

The expected output is similar to the following:

```python
Embeddings: [array([1.56808674e-01, -1.09599777e-01,  7.72696063e-02,  4.67760377e-02,
        1.53733594e-02, -7.59832468e-03, -4.85197157e-02, -5.92403952e-03,
       -6.97960034e-02, -7.70699885e-03,  2.15125885e-02,  6.11681007e-02,
       -2.92598619e-03,  4.61817719e-02, -4.55581546e-02, -2.96330396e-02,
...
        1.55469291e-02,  1.38307717e-02, -2.73534227e-02, -3.65062617e-02,
        2.18395051e-02,  1.39937887e-03,  4.28919913e-03, -2.25632302e-02,
       -6.35706726e-03, -2.17475481e-02,  2.49613114e-02, -6.89568091e-03])]
Dim 1024 (1024,)
```
