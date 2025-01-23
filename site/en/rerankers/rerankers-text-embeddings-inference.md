---
id: rerankers-text-embeddings-inference.md
order: 7
summary: Milvus supports the deployment of open source reranker models by TEI through the “TEIRerankFunction” class. This function allows you to efficiently score the relevance of query-document pairs.
title: text-embeddings-inference(TEI) - Rerankers
---

# text-embeddings-inference(TEI)

Text Embeddings Inference (TEI) is a comprehensive toolkit designed for efficient deployment and serving of open source text embeddings models. It enables high-performance extraction for the most popular models, including bge-reranker-large, roberta-base-go_emotions.

Key Features:
- Streamlined Deployment
- Efficient Resource Utilization
- Dynamic Batching
- Optimized Inference
- Safetensors weight loading
- Production-Ready

TEI Deployment Reference Documentation https://github.com/huggingface/text-embeddings-inference

To use this feature, install the necessary dependencies:

```bash
pip install --upgrade pymilvus
pip install "pymilvus[model]"
```

Then, instantiate the `TEIRerankFunction`:

```python
from pymilvus.model.reranker import TEIRerankFunction

tei_rf = TEIRerankFunction(
    api_url='http://127.0.0.1:8000'
)
```

__Parameters__:

- __api_url__ (_string_)

    TEI deployment api address.

Then, use the following code to rerank documents based on the query:

```python
query = "What event in 1956 marked the official birth of artificial intelligence as a discipline?"

documents = [
    "In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence.",
    "The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals.",
    "In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy.",
    "The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems."
]

results = tei_rf(
    query=query,
    documents=documents,
    top_k=3,
)

for result in results:
    print(f"Index: {result.index}")
    print(f"Score: {result.score:.6f}")
    print(f"Text: {result.text}\n")
```

The expected output is similar to the following:

```python
Index: 1
Score: 0.9971661
Text: The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals.

Index: 2
Score: 0.00809329
Text: In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy.

Index: 0
Score: 0.002491968
Text: The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.
```
