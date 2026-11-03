"""Practice reading related ORM objects."""

from rag.database import SessionLocal
from rag.models import Document


def main() -> None:
    """Retrieve a document and its related chunks."""

    with SessionLocal() as db:
        document = db.get(Document, 2)

        if document is None:
            print("Document not found.")
            return

        print(f"Document: {document.title}")

        for chunk in document.chunks:
            print(f"Chunk ID: {chunk.id}")
            print(f"Chunk index: {chunk.chunk_index}")
            print(f"Content: {chunk.content}")


if __name__ == "__main__":
    main()