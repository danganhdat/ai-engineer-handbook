# Budget tokens and build prompts

Build the input a model actually sees. You will keep the current question, reserve room for output, and select which conversation turns fit.

**Core · 65 minutes** · **Prerequisites** [Make a model call](../01-foundations/first-model.md).

## The problem

Documents and long conversations can exceed a model's context window. Even when everything fits, extra material can add cost, delay the response, and distract from relevant evidence.

## Understand the input

A tokenizer maps text to pieces called tokens. A token might be a word, part of a word, punctuation, or a piece of a string used in code. During generation a transformer uses attention to combine information from the available token positions and predicts the next token. An output can sound confident because it follows a likely language pattern. Its wording alone gives no proof that a claim is true.

Budget instructions, the latest user message, history, retrieved passages, and output. With a budget of 4,000 tokens, reserve 600 for output and 900 for fixed instructions and the question. The remaining 2,500 can be allocated to history and evidence. Count provider-specific overhead too.

## Your first working example

The exercise uses characters as a simple, deterministic stand-in. A hosted model needs the tokenizer or count facility appropriate to its model.


```python
--8<-- "examples/context.py"
```


Run `python -m examples.context`. Expect `['User: return an unopened headset']`. The latest complete turn fits. Adding the older turn would exceed the remaining budget.

## Extend and debug

Try a budget of 5. Expect no history. A negative budget signals that the fixed prompt itself exceeds the limit. Reduce the fixed prompt or reject the request with an explanation. In an actual conversation keep tool calls and their results together when selecting turns.

Test two instructions with the same input. First ask for a policy answer. Then specify the desired format and say to abstain if the supplied documents do not support it. Compare the outputs on both a supported question and a missing-evidence question. Use labeled samples when deciding which instruction works better.

## In production

Version instructions, output budget, and history selection together. Retain the current user question and constrain the number and length of chunks. Treat retrieved text as untrusted data. Separating it from instructions helps the model interpret it, while tool authorization still belongs in application code.

## Recap and next step

You can account for context, output budget, and the role of prompts in a repeatable experiment. [Next: Validate model output and tool calls](structured-outputs.md)

[OpenAI Cookbook tokenizer example](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
