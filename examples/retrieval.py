"""Rank an authorized set of chunks by shared keywords."""

import re

from examples.ingestion import DOCUMENTS, Chunk

STOP_WORDS = {"a", "an", "are", "do", "does", "how", "i", "the", "to", "within"}


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP_WORDS


def retrieve(query: str, owner: str, limit: int = 3) -> list[Chunk]:
    query_words = words(query)
    scores = [
        (len(query_words & words(chunk.text)), chunk)
        for chunk in DOCUMENTS
        if chunk.owner == owner
    ]
    scores.sort(key=lambda pair: (-pair[0], pair[1].id))
    return [chunk for score, chunk in scores if score > 0][:limit]


if __name__ == "__main__":
    for chunk in retrieve("headset returns", "training"):
        print(chunk.id)
