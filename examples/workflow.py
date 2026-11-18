"""Route a tool request with an explicit user-selected action."""

from typing import Literal

from examples.retrieval import retrieve


def run(
    action: Literal["search", "preview_note"], question: str, owner: str
) -> list[str]:
    if action == "search":
        return [chunk.id for chunk in retrieve(question, owner)]
    if action == "preview_note":
        return [f"Draft: {question}"]
    raise ValueError("Unknown action.")


if __name__ == "__main__":
    print(run("search", "headset returns", "training"))
    print(run("preview_note", "Review the returns policy.", "training"))
