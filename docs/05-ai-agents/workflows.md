# Build a deterministic tool workflow

Give Document Assistant two explicit actions. You will learn what makes a workflow deterministic before letting a model choose a tool.

**Core · 65 minutes** · **Prerequisites** [Validate model output and tool calls](../03-llm-engineering/structured-outputs.md) and [Search by keyword and meaning](../04-rag/retrieval.md).

## The problem

Answering a question is different from performing an operation. The application needs to know which capabilities it can call and which ones may change state.

## Your first working example

A workflow encodes steps and decisions in application code. This example chooses an action from an explicit input. Both actions are read-only because previewing a note returns text to the user without saving it.


```python
--8<-- "examples/workflow.py"
```


Run `python -m examples.workflow`. Expect `['returns-v1#1']` and `['Draft: Review the returns policy.']`.

## How it works

The search dispatch uses the caller scope. The preview builds a draft in memory. A real HTTP route would validate the action and derive the owner from the authenticated session.

An agent lets a model choose the next action based on the goal and results so far. Document Assistant can already answer policy questions with a fixed retrieve-then-answer workflow. Agentic choice is useful when the user describes a goal with unclear steps, such as locating relevant policy evidence and preparing a note for review.

## Extend and debug

Call `run("delete", "headset", "training")` from Python. Expect `ValueError: Unknown action.`. Observe that a type hint helps a type checker while the explicit runtime guard handles unexpected data. Try a valid search as `partner` and verify the returned chunk belongs to that owner.

## In production

Use operations with explicit, narrow inputs. A search tool should expose a query and limit and let application code decide the database scope. Give tool calls separate time budgets. Keep deterministic flows where the steps are known so you can measure and test them directly.

## Recap and next step

You established a tool interface and a baseline for comparison with agent behavior. [Next: Bound agent runs and approve writes](approvals.md)

[LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
