"""Evaluate retrieval and citation behavior on a tiny labeled fixture."""

from examples.retrieval import retrieve


def cited_answer(query: str, owner: str) -> tuple[str, list[str]]:
    matches = retrieve(query, owner, limit=1)
    if not matches:
        return "No supporting evidence was found.", []
    source = matches[0]
    return source.text, [source.id]


def main() -> None:
    cases = [
        ("headset returns", "training", "returns-v1#1"),
        ("standard shipping", "training", "shipping-v1#1"),
        ("headset returns", "partner", "partner-v1#1"),
    ]
    hits = sum(
        expected in {chunk.id for chunk in retrieve(query, owner, limit=1)}
        for query, owner, expected in cases
    )
    print(f"Recall@1: {hits / len(cases):.2f} ({hits}/{len(cases)})")
    for query in ("headset returns", "international warranty"):
        answer, citations = cited_answer(query, "training")
        print(answer, citations)


if __name__ == "__main__":
    main()
