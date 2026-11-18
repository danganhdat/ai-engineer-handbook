"""Send incremental text and a terminal event using SSE."""

import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from examples.api import Question

app = FastAPI(title="Document Assistant streaming fixture")


def event(name: str, data: dict[str, str]) -> str:
    return f"event: {name}\ndata: {json.dumps(data)}\n\n"


async def answer_events(question: Question) -> AsyncIterator[str]:
    yield event("delta", {"text": "You asked: "})
    await asyncio.sleep(0.1)
    yield event("delta", {"text": question.text})
    yield event("done", {})


@app.post("/answers/stream")
async def stream_answer(question: Question) -> StreamingResponse:
    return StreamingResponse(
        answer_events(question), media_type="text/event-stream"
    )
