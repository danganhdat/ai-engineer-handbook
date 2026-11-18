# Package the API with Docker

Read a Dockerfile for the API you already built. Follow the connection from a host port to Uvicorn inside the container.

**Supporting · 50 minutes** · **Prerequisites** [Expose a typed API](../02-backend/fastapi.md).

## The problem

An API can depend on a developer's Python version, packages, and files. An image describes the application filesystem and startup command. A container is a process started from that image with isolation and runtime settings.

## Walk through a Dockerfile

This teaching example packages the fixture API from the project root. Read each line before considering a build.


```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-examples.txt .
RUN pip install --no-cache-dir -r requirements-examples.txt
COPY examples/ ./examples/
USER 10001
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "examples.api:app", "--host", "0.0.0.0", "--port", "8000"]
```


The dependency layer can be reused when source files change. `COPY` reads files from the build context. Keep credentials and generated site files out of that context in a real project. An image can be pushed to a registry and identified by a digest of its content.

`EXPOSE` documents the intended container port. A mapping such as `127.0.0.1:8001:8000` would publish it on the host loopback address. The application listens on all container interfaces so traffic can reach it through that mapping.

## Practice and debugging

Imagine the image runs and logs “Uvicorn running” but the host gets connection refused. Compare the published host port with the request URL and the container port with the Uvicorn command. If Uvicorn binds only to `127.0.0.1` inside the container, it is listening on the wrong interface for published traffic.

How would the API reach a Postgres container? With Compose it would normally address the database by its service name on the shared network. A database volume keeps data across container replacements. Inside a container, `localhost` refers to that same container.

## In production

Pin and scan release images, run with a limited user, and pass runtime settings outside the image. A readiness check keeps traffic away until required dependencies are usable. A liveness check should detect a stuck process without turning a database outage into constant restarts.

## Recap and next step

You can read a container build and reason about ports, processes, and persistence. [Next: Map the application to Azure](architecture.md)

[Docker overview](https://docs.docker.com/get-started/docker-overview/), [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
