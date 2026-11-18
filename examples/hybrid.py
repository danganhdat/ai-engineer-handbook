"""Combine keyword results with a tiny fixed-vector search."""

from collections import defaultdict
from math import hypot

from examples.ingestion import DOCUMENTS, Chunk
from examples.retrieval import retrieve

# Two illustrative axes: how much a chunk is about returns and about shipping.
VECTORS = {
    "returns-v1#1": (1.0, 0.0),
    "returns-v1#2": (0.7, 0.2),
    "shipping-v1#1": (0.0, 1.0),
    "partner-v1#1": (1.0, 0.0),
}


def cosine(left: tuple[float, float], right: tuple[float, float]) -> float:
    dot = left[0] * right[0] + left[1] * right[1]
    return dot / (hypot(*left) * hypot(*right))


def hybrid_search(
    query: str, query_vector: tuple[float, float], owner: str
) -> list[Chunk]:
    candidates = [chunk for chunk in DOCUMENTS if chunk.owner == owner]
    semantic = sorted(
        candidates, key=lambda chunk: -cosine(query_vector, VECTORS[chunk.id])
    )[:2]
    scores: dict[str, float] = defaultdict(float)
    for ranking in (retrieve(query, owner, limit=2), semantic):
        for rank, chunk in enumerate(ranking, start=1):
            scores[chunk.id] += 1 / (60 + rank)
    return sorted(
        (chunk for chunk in candidates if chunk.id in scores),
        key=lambda chunk: (-scores[chunk.id], chunk.id),
    )


if __name__ == "__main__":
    result = hybrid_search("refund headphones", (1.0, 0.1), "training")
    print([chunk.id for chunk in result])
