# Learning roadmap

Follow the sidebar in order or use the prerequisites in each chapter to jump in. Budget about **29 hours** for reading and core exercises, with extra time for optional experiments. The numbers below are approximate.

| Part | Start here | Practice goal | Time |
| --- | --- | --- | --- |
| I. Foundations | [Build a Python CLI](01-foundations/python.md) | Explain the path from a command to a model API call | 2.5 hours |
| II. Backend | [Expose a typed API](02-backend/fastapi.md) | Validate requests, stream results, and enforce data ownership | 3.5 hours |
| III. LLM engineering | [Budget tokens and build prompts](03-llm-engineering/context.md) | Specify, validate, and measure model behavior | 3.5 hours |
| IV. RAG | [Ingest documents and build chunks](04-rag/ingestion.md) | Retrieve and cite evidence, then measure where retrieval fails | 4.25 hours |
| V. Agents | [Build a deterministic tool workflow](05-ai-agents/workflows.md) | Bound a tool loop and approve a write | 4 hours |
| VI. Containers and Azure | [Package the API with Docker](06-azure/containers.md) | Explain the path from image to a secure cloud request | 2 hours |
| VII. Delivery | [Describe infrastructure with Terraform](07-devops/terraform.md) | Review a plan and promote or roll back a revision | 2 hours |
| VIII. Production AI | [Observe quality, latency and cost](08-production-ai/observability.md) | Diagnose incidents and plan safe improvements | 5 hours |
| IX. Capstone | [Review the production design](09-capstone/design-review.md) | Defend the design with test evidence and a runbook | 2 hours |

## Choose the right depth

**Core** chapters ask you to build and debug. **Supporting** chapters ask you to use a tool or explain how it affects your system. **Optional** material helps you recognize when to consult specialists, for example for cluster administration, enterprise networking, multi-region recovery, or GPU inference optimization.

The progression follows a single application so that every new component addresses a problem you have already seen. Use the roadmaps for further practice after completing a part. [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/), [AI Engineer Roadmap](https://roadmap.sh/ai-engineer), [AI Agents Roadmap](https://roadmap.sh/ai-agents)
