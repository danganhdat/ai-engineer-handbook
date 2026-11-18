# Track model and prompt changes

Track the data, retrieval settings, prompts, and model used to produce a quality score. Reproduce the result before promoting a change.

**Core · 75 minutes** · **Prerequisites** [Choose a model and serving strategy](../03-llm-engineering/model-selection.md) and [Cite sources and evaluate RAG](../04-rag/evaluation.md).

## The problem

A retrieval experiment improved recall last week. Today nobody can tell whether the gain came from the embedding model, chunk size, corpus, or evaluation questions. Save enough metadata to compare like with like.

## Record an experiment

A run groups the parameters, metrics and artifacts from one execution. The following optional MLflow example uses the same three labeled retrieval cases as the RAG chapter. Run it from the project root in an environment with `python -m pip install "mlflow>=3,<4"` installed. Save it as `track_experiment.py` in that root.


```python
import mlflow

from examples.retrieval import retrieve

cases = [
    ("headset returns", "training", "returns-v1#1"),
    ("standard shipping", "training", "shipping-v1#1"),
    ("headset returns", "partner", "partner-v1#1"),
]
mlflow.set_tracking_uri("sqlite:///assistant-experiments.db")
mlflow.set_experiment("document-assistant")
with mlflow.start_run() as run:
    mlflow.log_params({"dataset": "policies-v1", "retriever": "lexical", "k": 1})
    hits = sum(
        source in {chunk.id for chunk in retrieve(query, owner, limit=1)}
        for query, owner, source in cases
    )
    mlflow.log_metric("recall_at_1", hits / len(cases))
    print(f"Recall@1: {hits / len(cases):.2f}")
```


Run `python track_experiment.py`. It creates or updates the local tracking database and records recall of `1.00`. On a clean environment it may also create an artifacts directory. For an application run, record the corpus revision, embedding deployment, prompts, selected chat deployment, input mix, and evaluator version.

## Extend and debug

Add the “refund headphones” case. Expect recall to drop to `0.75`. Change the dataset parameter to `policies-v2` so comparisons show that the benchmark changed. If the metrics differ between two runs with the same labels, verify the referenced dataset contents, pipeline code and dependency versions before attributing improvement to the model.

## In production

Evaluate candidate changes offline before release. Use limited online traffic to test latency and real input distributions once offline gates pass. Version artifacts and settings so operations can trace a release to its experiment. Track adoption, quality and cost after promotion. Azure Machine Learning managed online endpoints are an option when serving a model you package. Foundry hosted model deployments fit the main architecture when a managed API meets the requirement. Both still need change control and evaluation.

## Recap and next step

You defined an experiment record that connects an AI release to its evidence. [Next: Review the production design](../09-capstone/design-review.md)

[MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/), [Azure Machine Learning online endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/concept-endpoints-online)
