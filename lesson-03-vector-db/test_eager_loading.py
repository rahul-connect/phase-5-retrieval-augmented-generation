"""Practice eager loading related chunks."""

from rag.database import SessionLocal
from rag.repository import get_documents_with_chunks


def main() -> None:
    """Read documents and their chunks efficiently."""

    with SessionLocal() as db:
        documents = get_documents_with_chunks(db)

        for document in documents:
            print(f"Document: {document.title}")
            print(f"Number of chunks: {len(document.chunks)}")

            for chunk in document.chunks:
                print(f"  Chunk {chunk.chunk_index}: {chunk.content}")

            print("-" * 30)


if __name__ == "__main__":
    main()