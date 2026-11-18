# Stream an answer

Deliver pieces of an answer as they become available. Learn what changes when a response can fail after the HTTP headers have been sent.

**Core · 65 minutes** · **Prerequisites** [Expose a typed API](fastapi.md).

## The problem

An answer can take several seconds. Waiting for the full body makes the interface feel idle. Server-Sent Events, or SSE, use a text response with named events separated by blank lines. A client can show deltas as they arrive.

## Your first working example


```python
--8<-- "examples/streaming.py"
```


Start this example on port 8002 so it can run beside the previous one. In a second terminal, use the Python HTTP client to send a POST and print the received events. The `with` block closes the response on exit.


```console
python -m uvicorn examples.streaming:app --host 127.0.0.1 --port 8002
```




```python
import httpx

with httpx.stream(
    "POST", "http://127.0.0.1:8002/answers/stream",
    json={"text": "headset returns"},
) as response:
    response.raise_for_status()
    for line in response.iter_lines():
        print(line)
```


Expect two `delta` events and one `done` event. The short sleep stands in for waiting on a network call. While it awaits, the event loop can work on another request.

## Extend and debug

Send blank input. Expect `422` before the stream starts. Then remove the `done` event temporarily. The connection still ends cleanly at the HTTP level. The client should treat the answer as incomplete because it never received the application-level completion signal.

For a real provider stream, map provider errors to a terminal error event after streaming starts, and release its connection when the client disconnects. Browser clients can consume a POST stream with `fetch`. The built-in `EventSource` API opens a GET stream.

## In production

Track time to first token separately from total duration. Set deadlines for opening and reading the upstream stream. A bounded retry can help before any data is sent, subject to cost and request semantics. Retrying after a visible delta can duplicate or contradict text. Watch for reverse proxy buffering and match timeouts to the stream's idle behavior. Use a durable job for long-lived ingestion work that must survive API restarts.

## Recap and next step

You can distinguish a successful HTTP connection from a complete streamed answer. [Next: Keep state and enforce ownership](state.md)

[FastAPI streaming responses](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse), [Python asyncio](https://docs.python.org/3.11/library/asyncio.html)
