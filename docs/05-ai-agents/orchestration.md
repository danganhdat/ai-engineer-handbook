# Evaluate and orchestrate agents

Evaluate an agent by the actions it took and the state it left behind. See where a graph and persistent checkpoints add value.

**Core · 85 minutes** · **Prerequisites** [Bound agent runs and approve writes](approvals.md).

## The problem

An answer like “Done” can conceal a failed tool call or an unauthorized write. Inspect the trajectory, meaning the sequence of actions, results, and decisions.

## Run and debug a scripted agent

The callback supplies model-like tool proposals. Keeping it scripted makes the sequence predictable while you test the application loop.


```python
--8<-- "examples/agent.py"
```


Run `python -m examples.agent`. Expect a pause with zero saved notes. Replace the callback with one that always selects `search_documents`. Expect `step_limit` after three calls. Try an unknown tool and verify the loop exits without a write.

## Compare expected trajectories

| Case | Expected path | What to inspect |
| --- | --- | --- |
| Find a policy | Search → finish | Authorized citation IDs and time spent |
| Prepare a note | Search → propose → pause | Exact note proposal and zero saved notes |
| Rejected proposal | Pause → reject | No duplicate or delayed write |
| Misleading source text | Search → bounded decision | Tool allowlist and unchanged privileges |

Memory is information carried forward. Keep short-lived observations and persisted run state separate from long-term user preferences. Review what deserves to be retained and enforce tenant scoping and retention for both.

## Optional LangGraph exercise

Map search, propose, and decision to graph nodes. Use a checkpointer to save state, a stable thread ID scoped to the caller, and `interrupt()` to pause with a proposal. Resume with `Command(resume=decision)` after the application validates the actor. The node executes from its beginning when resumed, so put the durable write after the decision and make it idempotent. [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

The following optional fixture pauses a single node and then resumes it. Install `langgraph>=1,<2` in the tutorial environment and save the example as `graph_pause.py`.

```python
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict, total=False):
    note: str
    outcome: str


def review(state: State) -> dict[str, str]:
    approved = interrupt({"proposed_note": state["note"]})
    return {"outcome": "approved" if approved is True else "rejected"}


builder = StateGraph(State)
builder.add_node("review", review)
builder.add_edge(START, "review")
builder.add_edge("review", END)
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "training-run-1"}}
paused = graph.invoke({"note": "Review the returns policy."}, config)
assert "__interrupt__" in paused
resumed = graph.invoke(Command(resume=False), config)
print(resumed["outcome"])
```

Run `python graph_pause.py` and expect `rejected`. This uses an in-memory checkpoint, so the two invocations run in the same process. Change the thread ID for the resume call to see why the approval request must identify the right run.

## In production

Use one agent or a deterministic graph while it meets the goal. Consider specialized agents for genuinely independent subtasks with explicit handoffs. Measure extra model calls, lost context, and coordination failure before expanding. Trace tool names and outcomes, approval waits, budgets, and resume behavior without recording private arguments by default.

## Recap and next step

You can evaluate both the route through an agent and its final side effects. [Next: Package the API with Docker](../06-azure/containers.md)

[LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
