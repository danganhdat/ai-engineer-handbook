# AI Engineering Handbook

Build **Document Assistant**, an application that answers questions about documents, cites its sources, and asks for approval before it saves a note. You will start with a Python script and finish by reviewing how the system would run on Azure.

[Start with Python](01-foundations/python.md){ .md-button .md-button--primary }
[Browse the roadmap](roadmap.md){ .md-button }

## Start here

You need a terminal, a text editor, and Python 3.11 or later to run the core examples. If you can already build and test a Python API, start with [LLM engineering](03-llm-engineering/context.md). For document search, begin with [ingestion](04-rag/ingestion.md).

## What you will build

| Stage | What Document Assistant learns to do |
| --- | --- |
| Python and FastAPI | Accept a question, validate a request, and stream an answer |
| Models and RAG | Work within a context budget and cite authorized source material |
| Tools and agents | Propose a typed action, pause for approval, and record the outcome |
| Azure and operations | Choose services, promote a release, and diagnose quality and reliability failures |

!!! tip "Use one question as a running test"
    Ask “How many days do I have to return an unopened headset?” Rerun the question as you add retrieval, citations, authentication, and evaluation. Then ask about a policy missing from the sample documents. The system should make its uncertainty visible.

## How to use the chapters

Read the problem and run the main example. Predict what will happen in the debugging exercise before looking at the expected result. Core lessons build applied AI skills. Supporting lessons teach the infrastructure you need to reason about an AI application. Optional sections cover specialized tools and hosted services.
