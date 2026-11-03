
"""Practice inserting related document and chunk records."""

from rag.database import SessionLocal
from rag.repository import add_document_with_chunk


def main() -> None:
    """Insert one document with one dummy embedding."""

    dummy_embedding = [0.0] * 767 + [1.0]

    with SessionLocal.begin() as db:
        document = add_document_with_chunk(
            db=db,
            title="Relationship Practice",
            content="Python supports functions and classes.",
            chunk_content="Python supports functions and classes.",
            embedding=dummy_embedding,
        )

        db.flush()

        print(f"Document ID: {document.id}")
        print(f"Chunk ID: {document.chunks[0].id}")
        print(f"Chunk document ID: {document.chunks[0].document_id}")


if __name__ == "__main__":
    main()
