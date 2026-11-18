"""Turn paragraph-shaped synthetic policies into addressable chunks."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    id: str
    owner: str
    text: str


def chunk_document(document_id: str, owner: str, text: str) -> list[Chunk]:
    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    return [
        Chunk(f"{document_id}#{position}", owner, paragraph)
        for position, paragraph in enumerate(paragraphs, start=1)
    ]


DOCUMENTS = chunk_document(
    "returns-v1", "training", "Unopened headset returns are accepted within 30 days."
    "\n\nSend a receipt with the unopened item.",
) + chunk_document(
    "shipping-v1", "training", "Standard shipping takes five business days."
) + chunk_document(
    "partner-v1", "partner", "Unopened headset returns are accepted within 90 days."
)


if __name__ == "__main__":
    for chunk in DOCUMENTS[:2]:
        print(f"{chunk.id}: {chunk.text}")
