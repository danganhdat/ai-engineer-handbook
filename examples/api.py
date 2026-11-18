"""A Document Assistant HTTP endpoint with a deterministic model."""

from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

from examples.model_call import ask

app = FastAPI(title="Document Assistant")


class Question(BaseModel):
    text: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=1, max_length=500
    )]


class Answer(BaseModel):
    answer: str


@app.post("/answers")
def create_answer(question: Question) -> Answer:
    return Answer(answer=ask(question.text))
