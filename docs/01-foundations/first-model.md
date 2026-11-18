# Make a model call

Replace the CLI's echo with a model interface. Start with a fixture and optionally send the same question to a deployed model in Microsoft Foundry.

**Core · 55 minutes** · **Prerequisites** The first two foundations chapters. The default example uses Python only.

## The problem

Model requests have credentials, latency, and variable output. The rest of Document Assistant needs a predictable way to ask a question while we learn how to handle those moving parts.

## Run a fixture first

A fixture is a known input or response used to exercise code. The fixture lets you check the CLI without sending a request over the network.


```python
--8<-- "examples/model_call.py"
```




```console
python -m examples.model_call "What is the return policy?"
```

Expect `Fixture response: use a source document to verify the answer.`


## How a hosted call works

The hosted branch sends the question and a short instruction to a deployment. During inference the model generates tokens based on its input. The API returns a response object with a status and output items. The SDK assembles text from the response as `output_text`. The example checks for a completed response so an incomplete result does not pass as a finished answer.

??? example "Optional hosted call"
    You need an Azure subscription, a supported Azure OpenAI model deployment, an endpoint, and a permitted API key. Confirm region and quota before sending requests, which may incur usage charges. Install the SDK with `python -m pip install "openai>=2,<3"`. Set `AZURE_OPENAI_ENDPOINT` to your resource URL, `AZURE_OPENAI_DEPLOYMENT` to your deployment name, and `AZURE_OPENAI_API_KEY` through your environment. Then run `python -m examples.model_call "What is the return policy?" --hosted`. Expect a short answer whose wording can vary. Give the model a synthetic question so the exercise does not transmit private policy text. [Azure OpenAI Responses API](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses)

## Practice and debugging

Remove `AZURE_OPENAI_DEPLOYMENT` and run the hosted path. A missing setting causes a local `KeyError` before the model request. With a configured deployment, an upstream error can identify an invalid credential, unknown deployment, or exhausted rate limit. Record the status and provider request ID when available.

## In production

Set a request deadline and handle transient failures under that deadline. Keep secrets separate from logs and source code. Consider Microsoft Entra authentication for deployed workloads. Review your data handling requirements before sending document content to an inference service.

## Recap and next step

You can swap the model behind one application function and distinguish local configuration from upstream behavior. [Next: Expose a typed API](../02-backend/fastapi.md)

[Foundry endpoints](https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/concepts/endpoints)
