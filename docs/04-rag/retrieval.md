# Search by keyword and meaning

Build the first search baseline and compare it with vector and hybrid retrieval. Document permissions affect the candidate set before ranking begins.

**Core · 85 minutes** · **Prerequisites** [Ingest documents and build chunks](ingestion.md).

## The problem

An exact match can find a product code, yet users often describe the same item with a synonym. A semantic search can help with synonyms. You still need a permission boundary shared by every retrieval strategy.

## Your first working example

The fixture scores chunks by the number of query terms they share. Ownership is checked before a chunk receives a score.


```python
--8<-- "examples/retrieval.py"
```


Run `python -m examples.retrieval`. Expect `returns-v1#1` only. The partner chunk contains the same search terms and belongs to a different owner.

## Add vector search

An embedding is a vector of numbers. Compare query and document vectors produced by the same model and configuration. Cosine distance measures their direction relative to one another. Lower distance means a closer match. The PostgreSQL excerpt assumes pgvector is installed, `owner_id` is a UUID, and all stored vectors use the query's dimensions.


```sql
PREPARE vector_search (uuid, vector) AS
SELECT id, text, embedding <=> $2 AS distance
FROM chunks
WHERE owner_id = $1
ORDER BY embedding <=> $2
LIMIT 5;
```


Connect the owner parameter to authenticated identity. Start with exact search for a small corpus. Measure recall and latency before adopting an approximate index such as HNSW. Selective filters can leave approximate search with too few matches, so inspect filtered recall on a representative dataset.

## Extend and debug

Search for “refund headphones”. Expect the keyword fixture to return no results. Add this query to the labeled dataset and compare it with semantic retrieval in a real system. A synonym can be semantically close without being an exact match.

A hybrid ranker combines keyword and vector candidates. Reciprocal rank fusion adds values such as `1 / (60 + rank)` from each ranked list. It uses positions and avoids assuming the raw keyword and vector scores share a scale. Reranking can apply a stronger relevance scorer to a small pool at the cost of an extra inference step.

The following exercise gives the query and chunks illustrative vectors so you can examine rank fusion without a hosted model.

```python
--8<-- "examples/hybrid.py"
```

Run `python -m examples.hybrid`. Expect `['returns-v1#1', 'returns-v1#2']`. Change the query vector to `(0.1, 1.0)` and rerun. Shipping should rank first even though the text is still “refund headphones”. In a real system the same embedding model generates both document and query vectors, so this mismatch would be a test for a configuration or data-flow error.

## In production

Apply tenant and document permissions to each retriever. Keep them in force when resolving a citation. PostgreSQL and pgvector share existing metadata and operational tooling. Foundry IQ (Azure AI Search) is an optional comparison when managed indexing or independent search scaling solves a measured need.

## Recap and next step

You implemented a controlled lexical baseline and traced the vector and hybrid alternatives. [Next: Cite sources and evaluate RAG](evaluation.md)

[pgvector](https://github.com/pgvector/pgvector), [Azure AI Search hybrid search](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview)
