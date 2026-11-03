
"""Database operations for RAG documents."""

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from rag.models import Chunk, Document
from rag.query_preprocessing import prepare_keyword_query

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



def keyword_search(
    db: Session,
    query: str,
    top_k: int = 20,
    category: str | None = None,
) -> list[tuple[Chunk, str, float]]:
    """Find chunks ranked by PostgreSQL full-text search."""

    #tsquery = func.plainto_tsquery("english", query)
    #tsquery = func.websearch_to_tsquery("english", query)

    prepared_query = prepare_keyword_query(query)
    tsquery = func.websearch_to_tsquery("english", prepared_query)

    rank = func.ts_rank(Chunk.content_tsv, tsquery).label("rank")

    stmt = (
        select(Chunk, Document.title, rank)
        .join(Chunk.document)
        .where(Chunk.content_tsv.op("@@")(tsquery))
    )

    if category is not None:
        stmt = stmt.where(Document.category == category)

    stmt = stmt.order_by(rank.desc()).limit(top_k)

    rows = db.execute(stmt).all()

    return [
        (chunk, title, float(score))
        for chunk, title, score in rows
    ]


def search_similar_chunks_with_filter(
    db: Session,
    query_embedding: list[float],
    top_k: int = 5,
    category: str | None = None,
) -> list[tuple[Chunk, str, float]]:

    distance = Chunk.embedding.cosine_distance(query_embedding)

    stmt = (
        select(Chunk, Document.title, distance.label("distance"))
        .join(Chunk.document)
    )

    if category is not None:
        stmt = stmt.where(Document.category == category)

    stmt = stmt.order_by(distance.asc()).limit(top_k)

    rows = db.execute(stmt).all()

    return [
        (chunk, title, float(score))
        for chunk, title, score in rows
    ]


def ingest_document(
    db: Session,
    title: str,
    content: str,
    source: str | None,
    category: str | None,
    chunk_contents: list[str],
    embeddings: list[list[float]],
) -> Document:
    """Store a document and all its chunks atomically."""

    if len(chunk_contents) != len(embeddings):
        raise ValueError("Each chunk must have a matching embedding")

    document = Document(
        title=title,
        content=content,
        source=source,
        category=category,
    )

    for index, (chunk_text, vector) in enumerate(
        zip(chunk_contents, embeddings)
    ):
        chunk = Chunk(
            chunk_index=index,
            content=chunk_text,
            embedding=vector,
        )

        document.chunks.append(chunk)

    try:
        db.add(document)
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(document)

    return document


def list_documents_with_chunk_counts(
    db: Session,
) -> list[tuple[Document, int]]:
    """List documents and their chunk counts, newest first."""

    stmt = (
        select(
            Document,
            func.count(Chunk.id).label("chunk_count"),
        )
        .outerjoin(
            Chunk,
            Chunk.document_id == Document.id,
        )
        .group_by(Document.id)
        .order_by(Document.created_at.desc())
    )

    return list(db.execute(stmt).all())