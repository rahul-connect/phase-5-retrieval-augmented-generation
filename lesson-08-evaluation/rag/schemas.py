"""Request and response schemas for the RAG API."""

from datetime import datetime

from pydantic import BaseModel, Field


# Request schemas

class CreateDocumentRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    content: str = Field(min_length=1)
    source: str | None = Field(default=None, max_length=1000)
    category: str | None = Field(default=None, max_length=50)


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)
    category: str | None = Field(default=None, max_length=50)


# Response schemas

class DocumentSummary(BaseModel):
    id: int
    title: str
    source: str | None
    category: str | None
    created_at: datetime
    chunk_count: int


class CreateDocumentResponse(BaseModel):
    id: int
    title: str
    chunk_count: int
    message: str


class RetrievedChunk(BaseModel):
    title: str
    content: str
    score: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks: list[RetrievedChunk]
    prompt_tokens: int
    completion_tokens: int
    model: str