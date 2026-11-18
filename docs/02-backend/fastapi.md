# Expose a typed API

Expose Document Assistant as a JSON API. The request schema gives callers a predictable interface and catches invalid input before it reaches the model.

**Core · 60 minutes** · **Prerequisites** [Make a model call](../01-foundations/first-model.md) and the API dependencies below.

## The problem

A CLI works for one terminal. A web client or automation needs an address, an HTTP method, and a defined request and response. FastAPI routes requests to functions. Pydantic checks the shape and constraints of data at the boundary.

## Your first working example

Install the API dependencies with `python -m pip install -r requirements-examples.txt` in your environment.


```python
--8<-- "examples/api.py"
```


Start the tutorial server from the root.


```console
python -m uvicorn examples.api:app --host 127.0.0.1 --port 8001
```


Open `http://127.0.0.1:8001/docs`. Expand `POST /answers`, choose **Try it out**, and send the following body.


```json
{"text":"What is the return policy?"}
```


Expect HTTP `200` and `{"answer":"Fixture response: use a source document to verify the answer."}`.

## How it works

Uvicorn passes an HTTP request to the ASGI application. FastAPI parses the JSON body and builds a `Question`. The model strips whitespace and applies a length bound. FastAPI calls the route and serializes the returned `Answer`. The same type definitions contribute to the OpenAPI description that powers the browser UI.

## Extend and debug

Submit `{"text":"   "}`. Expect HTTP `422` and a validation error pointing to `body.text`. Send a request with the wrong method and compare the `405` response. A client test can inspect both responses without binding a port.


```python
from fastapi.testclient import TestClient
from examples.api import app

with TestClient(app) as client:
    response = client.post("/answers", json={"text": "   "})
    assert response.status_code == 422
```


## In production

Use dependency injection for a model client and caller identity. Use middleware for concerns such as request IDs and timing. A synchronous route is appropriate for this fixture. An async route can wait for an async network client while the server handles other requests. Keep model credentials and internal exceptions out of API responses.

## Recap and next step

You exposed a typed HTTP interface and verified its validation boundary. [Next: Stream an answer](streaming.md)

[FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/), [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
