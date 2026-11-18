# Observe quality, latency and cost

Trace a single answer from HTTP through retrieval to inference. Pick measurements that tell you why quality or latency changed.

**Core · 70 minutes** · **Prerequisites** [Cite sources and evaluate RAG](../04-rag/evaluation.md) and [Stream an answer](../02-backend/streaming.md).

## The problem

Users report that answers are slower and sometimes unsupported. One log line showing `200` cannot tell which dependency was slow or whether the answer was grounded.

## Understand the signals

A log records an event. A metric aggregates numerical observations. A trace links work across components, and a span describes one operation within it. Send a request or trace ID across the API and worker boundary so an operator can relate events without placing private content in logs.

## Read a trace

The synthetic trace below describes one successful answer. Nested spans may overlap, so compare their boundaries instead of adding every duration.


```text
trace 63c2  POST /answers          1350 ms  status=200
  embed_query                       130 ms
  retrieve                          30 ms  candidates=3
  generate                        1160 ms  first_token=610 ms
                                               input_tokens=850 output_tokens=93
```


Generation dominates this trace. Use aggregate histograms to find out whether that pattern holds at p50 and p95. First-token time captures when streaming starts. End-to-end time captures completion. Record model deployment, prompt version, retrieval strategy and status with stable, low-cardinality tags. Keep request IDs in traces or logs, since using them as metric labels creates a separate series for each request.

## Extend and debug

At 10:00, p95 latency rises and model `429` responses increase. Retrieval latency and database connections stay steady. Start with model concurrency, provider quota, and retries. Check if retries amplify request volume. Limit concurrency or fail gracefully under a deadline and verify that p95 and successful answers recover. If retrieval scores or authorized candidate counts drop too, inspect indexing and filters separately.

## In production

Set alerts that map to action, such as sustained error rate or document queue age. Track tokens and estimate cost with the input and output rates of the deployed model. Confirm estimates against billing and keep usage budgets. Use Azure Monitor and Application Insights to correlate traces and platform signals. Record metadata by default and review any policy to sample prompt or document content before enabling it.

## Recap and next step

You can follow evidence from one trace to aggregate latency, errors, quality, and cost. [Next: Measure performance and cache results](performance.md)

[OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/), [Application Insights OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable)
