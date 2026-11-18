# Validate model output and tool calls

Use Pydantic to validate a model-suggested search. The model proposes arguments, and your code decides whether to execute the tool.

**Core · 70 minutes** · **Prerequisites** [Expose a typed API](../02-backend/fastapi.md) and the dependencies in `requirements-examples.txt`.

## The problem

A caller expects a search query and a small result limit. The model might return prose, a wrong type, or a plausible-looking request outside the caller's permissions.

## Your first working example


```python
--8<-- "examples/structured.py"
```


Run `python -m examples.structured`. Expect `{"query":"headset","limit":2}` followed by `Rejected: limit`. Strict validation catches an incoming string where code expects an integer. Forbidding extras helps expose unexpected fields before a developer mistakes them for supported arguments.

## How it fits

With structured outputs, a supported provider can constrain generated data to a JSON Schema. Use that feature when downstream code needs a stable structure. With function calling, the response includes a proposed tool name and arguments. Dispatch only registered tools, validate arguments locally, and attach the actual caller identity to the call.

Document Assistant sends a typed search definition, receives a call such as `search_documents`, validates its arguments, and runs an ownership-filtered search. It can pass the tool result back to the model alongside the corresponding call ID. The tool's output is also data and can contain untrusted text.

## Extend and debug

Replace the result limit with `50`, add an `owner_id` property, or send malformed JSON. Check what error each input produces. For the first two, expect a range error and an extra-field error. A valid limit and query can still yield no results. Give that case a distinct outcome.

## In production

Handle refusals and truncated responses separately from schema failures. A provider may support a subset of JSON Schema. Use the versioned API reference for the chosen deployment and exercise its real outputs with an integration test. Give tools clear descriptions, bounded inputs, and narrowly scoped permissions.

## Recap and next step

You validated model output and separated argument validation from execution authority. [Next: Choose a model and serving strategy](model-selection.md)

[Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/), [Foundry structured outputs](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
