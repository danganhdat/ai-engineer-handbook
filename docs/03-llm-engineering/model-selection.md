# Choose a model and serving strategy

Pick an inference strategy using measurements from the kind of questions Document Assistant actually receives.

**Core · 75 minutes** · **Prerequisites** [Budget tokens and build prompts](context.md) and [Validate model output and tool calls](structured-outputs.md).

## The problem

A stronger model can improve a difficult answer while making an ordinary request slower or more expensive. A large context window can make a design possible without making it efficient. Set acceptance criteria before choosing a deployment.

## Understand serving

Inference is model execution to produce a prediction or response. Request time includes queueing, processing the input, generating output, and network transfers. An inference server can batch requests to improve throughput, while waiting for a batch can increase latency for one user. Streaming exposes the first output sooner. It does not reduce all the work the server performs.

Managed inference gives you an endpoint and leaves much of the serving operation to the provider. Self-hosted inference can give you more control over hardware, data placement, and runtime tuning. It also makes capacity planning, patches, model licensing and operational coverage your responsibility.

## Work a model selection example

The table is synthetic. Both candidates answered the same 50 questions with the same retrieval pipeline. A grounded answer is supported by the retrieved evidence.

| Candidate | Grounded answers | p95 response time | Cost per 1,000 questions |
| --- | ---: | ---: | ---: |
| A | 45/50 | 1.8 s | $1.40 |
| B | 48/50 | 3.1 s | $4.80 |

Require at least 90% grounded answers, p95 under 2.5 seconds, and cost under $3. Candidate A meets these thresholds. Before adopting it, inspect which five questions it missed. Aggregate quality can hide a failure on a critical policy.

## Extend and debug

Candidate A fails questions about a policy version absent from the index. Compare the retrieved chunks to the labeled source before changing the model. Expect retrieval recall to fail for the missing version. Add the correct document, reindex, and repeat the same comparison.

Use prompting for an improved instruction or format. Add retrieval when current external facts or citations matter. Consider fine-tuning for a durable behavior change when prompt and data improvements have plateaued and you have representative training and evaluation examples.

## In production

Version the selected deployment, prompts, and evaluator together. Set quotas and deadlines. Watch rate-limit responses and the effect of retries on throughput and cost. Test the fallback's behavior on the same questions before routing real requests to it.

## Recap and next step

You selected a model under explicit quality, latency, and cost constraints. [Next: Ingest documents and build chunks](../04-rag/ingestion.md)

[Foundry model catalog](https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview), [Azure Machine Learning online endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/concept-endpoints-online)
