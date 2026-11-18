# Ingest documents and build chunks

Turn documents into searchable records with stable citation IDs. Start with paragraphs and work through how a larger ingestion pipeline would parse and embed them.

**Core · 75 minutes** · **Prerequisites** [Keep state and enforce ownership](../02-backend/state.md).

## The problem

Passing each whole file to the model wastes context. Searching a file needs smaller units of evidence that still make sense when read independently and can be traced back to the original.

## Your first working example

A chunk is a portion of source text that can be retrieved on its own. For short synthetic documents, treat each paragraph as a chunk.


```python
--8<-- "examples/ingestion.py"
```


Run `python -m examples.ingestion`. Expect the following IDs and text.


```text
returns-v1#1: Unopened headset returns are accepted within 30 days.
returns-v1#2: Send a receipt with the unopened item.
```


## How chunking works

A parser turns bytes into text and source locations. A chunker chooses boundaries. An embedding model maps each chunk to a vector that a retrieval engine can compare with query vectors. Store the chunk ID, document version, owner, source location and embedding model alongside the text and vector. Stable IDs make citations testable and help with retries.

For Markdown, a heading plus paragraphs can preserve section meaning. For PDFs with selectable text, use page numbers and inspect reading order. Scanned PDFs typically need optical character recognition. A parser can succeed while producing unusable text, so verify text length and review sample pages before indexing.

## Extend and debug

Move the return deadline into its own paragraph. Retrieve on “headset returns” in the next lesson and inspect whether the returned paragraph still includes the number. If it does not, try a section-based chunk or a small overlap. Overlap preserves context at a boundary and can increase duplicates, storage and cost.

## In production

Set file size and parser limits. Record extraction and indexing status separately. Avoid indexing a partial upload. Use a document revision and deterministic chunk IDs so a retried job overwrites its own output. Track embedding model changes and rebuild the index when you change embedding space.

## Recap and next step

You created stable chunks and understand how parser and chunk decisions affect retrieval. [Next: Search by keyword and meaning](retrieval.md)

[pypdf text extraction](https://pypdf.readthedocs.io/en/stable/user/extract-text.html), [Foundry embeddings](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/embeddings)
