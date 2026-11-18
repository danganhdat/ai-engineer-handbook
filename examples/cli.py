"""Ask the fixture a question from your terminal."""

import argparse


def answer(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Enter a question.")
    return f"You asked: {question}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    args = parser.parse_args()
    try:
        print(answer(args.question))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
