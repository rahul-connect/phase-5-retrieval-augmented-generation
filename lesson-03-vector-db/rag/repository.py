
"""Database operations for RAG documents."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from rag.models import Chunk, Document


def get_all_documents(db: Session) -> list[Document]:
    """Retrieve all documents ordered by ID."""

    stmt = select(Document).order_by(Document.id)

    return list(db.scalars(stmt).all())


def get_document_by_id(
    db: Session,
    document_id: int,
) -> Document | None:
    """Retrieve a document by its primary key."""

    return db.get(Document, document_id)



def add_document_with_chunk(
    db: Session,
    title: str,
    content: str,
    chunk_content: str,
    embedding: list[float],
) -> Document:
    """Stage a document and its first chunk in the session."""

    document = Document(
        title=title,
        content=content,
    )

    chunk = Chunk(
        chunk_index=0,
        content=chunk_content,
        embedding=embedding,
    )

    document.chunks.append(chunk)

    db.add(document)

    return document


def get_documents_with_chunks(db: Session) -> list[Document]:
    """Retrieve documents with their chunks eagerly loaded."""

    stmt = (
        select(Document)
        .options(selectinload(Document.chunks))
        .order_by(Document.id)
    )

    return list(db.scalars(stmt).all())


def get_chunks_with_document_titles(
    db: Session,
) -> list[tuple[Chunk, str]]:
    """Retrieve chunks together with their document titles."""

    stmt = (
        select(Chunk, Document.title)
        .join(Chunk.document)
        .order_by(Chunk.id)
    )

    return list(db.execute(stmt).all())



def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    top_k: int = 5,
) -> list[tuple[Chunk, str, float]]:
    """Find chunks ordered by cosine distance."""

    distance = Chunk.embedding.cosine_distance(query_embedding)

    stmt = (
        select(
            Chunk,
            Document.title,
            distance.label("distance"),
        )
        .join(Chunk.document)
        .order_by(distance)
        .limit(top_k)
    )

    rows = db.execute(stmt).all()

    results = []

    for chunk, title, score in rows:
        result = (
            chunk,
            title,
            float(score),
        )

        results.append(result)

    return results
