"""Use scripted model proposals to exercise a bounded tool loop."""

from collections.abc import Callable

from examples.approvals import NoteStore, Proposal
from examples.retrieval import retrieve

ChooseTool = Callable[[list[str]], tuple[str, str]]


def run(
    run_id: str, owner: str, choose_tool: ChooseTool, store: NoteStore
) -> str:
    observations: list[str] = []
    for _ in range(3):
        tool, argument = choose_tool(observations.copy())
        if tool == "finish":
            return "finished"
        if not argument.strip() or len(argument) > 500:
            return "invalid_arguments"
        if tool == "search_documents":
            matches = retrieve(argument, owner, limit=2)
            observations.extend(chunk.id for chunk in matches)
        elif tool == "propose_note":
            store.propose(Proposal(run_id, owner, argument))
            return "awaiting_approval"
        else:
            return "unknown_tool"
    return "step_limit"


if __name__ == "__main__":
    def choose_tool(observations: list[str]) -> tuple[str, str]:
        if observations:
            return "propose_note", f"Review {observations[0]}."
        return "search_documents", "headset returns"

    store = NoteStore()
    print(run("run-1", "training", choose_tool, store))
    print(f"Saved notes: {len(store.notes)}")
