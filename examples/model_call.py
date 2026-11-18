"""Ask a fixture or a deployed Azure OpenAI model the same question."""

import argparse
import os

from examples.cli import answer as validate_question


def ask(question: str, *, hosted: bool = False) -> str:
    validate_question(question)
    if not hosted:
        return "Fixture response: use a source document to verify the answer."

    from openai import OpenAI

    resource = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    with OpenAI(
        base_url=f"{resource}/openai/v1/",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        timeout=15,
        max_retries=0,
    ) as client:
        response = client.responses.create(
            model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            input=question,
            instructions="Answer briefly and say when you are unsure.",
            max_output_tokens=250,
            store=False,
        )
        if response.status != "completed" or not response.output_text:
            raise RuntimeError(f"No complete text answer (status: {response.status}).")
        return response.output_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--hosted", action="store_true")
    args = parser.parse_args()
    print(ask(args.question, hosted=args.hosted))
