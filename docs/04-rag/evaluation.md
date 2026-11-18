# Cite sources and evaluate RAG

Make answers verifiable and measure whether the retriever finds known evidence. Separate a ranking failure from a generation or citation failure.

**Core · 95 minutes** · **Prerequisites** [Search by keyword and meaning](retrieval.md).

## The problem

An answer can be wrong because the right chunk was missing or because the model ignored it. Evaluating final text alone makes it hard to tell where to fix the application.

## Your first working example

This fixture returns the leading authorized passage as the answer. Its narrow behavior makes retrieval and citations easy to inspect without a model.


```python
--8<-- "examples/evaluation.py"
```


Run `python -m examples.evaluation`. Expect these results.


```text
Recall@1: 1.00 (3/3)
Unopened headset returns are accepted within 30 days. ['returns-v1#1']
No supporting evidence was found. []
```


## Interpret the result

For each test question, recall at `k` is the fraction of its labeled relevant chunks found in the first `k` retrieval results. The dataset here has one relevant chunk per question. The printed number averages recall over three labeled queries.

For a generated answer, measure whether its factual claims are supported. Verify citation IDs belong to the supplied authorized candidates and review whether those passages support the claims they are attached to. An existing citation can still be the wrong source. Track abstention on unanswerable questions separately.

## Extend and debug

Add the following item to `cases` and rerun.


```python
("refund headphones", "training", "returns-v1#1"),
```


The score drops to `0.75 (3/4)`. Inspect the query terms and evidence to see why. Repeat with synonyms or a hybrid implementation. Include documents with similar wording and different policy dates so the benchmark catches plausible wrong answers.

## In production

Save the question, allowed scope, expected evidence and dataset version together. Measure recall, citation validity, and grounded answers by slice. Use representative held-out questions before release and privacy-reviewed samples afterward. Pair human reviews with automated checks for important or ambiguous cases.

## Recap and next step

You diagnosed one retrieval failure and defined separate quality checks for generation. [Next: Build a deterministic tool workflow](../05-ai-agents/workflows.md)

[Microsoft Foundry RAG evaluators](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators)
