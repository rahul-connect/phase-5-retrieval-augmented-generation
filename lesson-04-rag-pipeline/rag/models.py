
"""SQLAlchemy models for the RAG system."""

from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


EMBEDDING_DIM = 768


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class Document(Base):
    """A source document that gets chunked and embedded."""

    __tablename__ = "rag_documents"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(String(500))

    content: Mapped[str] = mapped_column(Text)

    source: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    chunks: Mapped[list["Chunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Chunk(Base):
    """A chunk of a document with its embedding."""

    __tablename__ = "rag_chunks"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rag_documents.id", ondelete="CASCADE"),
        index=True,
    )

    chunk_index: Mapped[int] = mapped_column(Integer)

    content: Mapped[str] = mapped_column(Text)

    embedding: Mapped[list[float]] = mapped_column(
        Vector(EMBEDDING_DIM)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    document: Mapped["Document"] = relationship(
        back_populates="chunks"
    )
