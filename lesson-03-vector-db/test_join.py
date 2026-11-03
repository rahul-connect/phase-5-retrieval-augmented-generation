"""Practice querying chunks and document titles using JOIN."""

from rag.database import SessionLocal
from rag.repository import get_chunks_with_document_titles


def main() -> None:
    """Display each chunk alongside its parent document title."""

    with SessionLocal() as db:
        rows = get_chunks_with_document_titles(db)

        for chunk, document_title in rows:
            print(f"Document: {document_title}")
            print(f"Chunk index: {chunk.chunk_index}")
            print(f"Content: {chunk.content}")
            print("-" * 30)


if __name__ == "__main__":
    main()