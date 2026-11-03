from sqlalchemy.orm import Session

from rag.chunking import chunk_recursive
from rag.embeddings import embed_text
from rag.models import Document, Chunk
from rag.repository import get_all_documents
from rag.database import SessionLocal


"""This function is useful when we're ingesting a brand-new document.
However, the assignment has us insert the original documents directly into rag_documents first."""
def ingest_document(
    db: Session,
    title: str,
    content: str,
    chunk_size: int = 500,
) -> Document:
    """Chunk, embed, and store a document."""
    
    chunks = chunk_recursive(content, chunk_size)

    document = Document(title=title, content=content)

    for index, chunk_text in enumerate(chunks):
        embedding = embed_text(chunk_text)
        chunk = Chunk(
            chunk_index=index,
            content=chunk_text,
            embedding=embedding,
        )

        document.chunks.append(chunk)

    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def ingest_existing_documents(
    db: Session,
    chunk_size: int = 500,
) -> None:
    """Generate and store chunks for existing documents."""

    documents = get_all_documents(db)

    for document in documents:
        if document.chunks:
            continue

        chunks = chunk_recursive(document.content, chunk_size)

        for index, chunk_text in enumerate(chunks):
            embedding = embed_text(chunk_text)

            chunk = Chunk(
                chunk_index=index,
                content=chunk_text,
                embedding=embedding,
            )

            document.chunks.append(chunk)

        db.commit()


if __name__ == "__main__":
    with SessionLocal() as db:
        ingest_existing_documents(db)