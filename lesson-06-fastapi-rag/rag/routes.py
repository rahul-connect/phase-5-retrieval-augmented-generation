"""HTTP endpoints for the RAG service."""

from fastapi import APIRouter

from rag import repository
from rag.dependencies import DbSession
from rag.schemas import DocumentSummary
from rag.chunking import chunk_recursive
from rag.embeddings import embed_text
from rag.schemas import CreateDocumentRequest, CreateDocumentResponse
from rag.rag_pipeline import answer_question
from rag.schemas import QueryRequest, QueryResponse, RetrievedChunk

router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    """Basic service health check."""
    return {
        "service": "RAG API",
        "status": "running",
        "version": "0.1.0",
    }


@router.get("/documents", response_model=list[DocumentSummary])
def list_documents(db: DbSession) -> list[DocumentSummary]:
    """Return documents with their chunk counts."""

    rows = repository.list_documents_with_chunk_counts(db)

    return [
        DocumentSummary(
            id=doc.id,
            title=doc.title,
            source=doc.source,
            category=doc.category,
            created_at=doc.created_at,
            chunk_count=chunk_count,
        )
        for doc, chunk_count in rows
    ]


@router.post(
    "/documents",
    response_model=CreateDocumentResponse,
    status_code=201,
)
def create_document(
    request: CreateDocumentRequest,
    db: DbSession,
) -> CreateDocumentResponse:
    """Chunk, embed, and store a new document."""

    # Step 1: Split the document into chunks.
    chunk_texts = chunk_recursive(
        request.content,
        chunk_size=500,
    )

    # Step 2: Generate embeddings before database writes.
    embeddings = [
        embed_text(text, task_type="RETRIEVAL_DOCUMENT")
        for text in chunk_texts
    ]

    # Step 3: Persist the document and its chunks.
    document = repository.ingest_document(
        db=db,
        title=request.title,
        content=request.content,
        source=request.source,
        category=request.category,
        chunk_contents=chunk_texts,
        embeddings=embeddings,
    )

    # Step 4: Return the ingestion result.
    return CreateDocumentResponse(
        id=document.id,
        title=document.title,
        chunk_count=len(chunk_texts),
        message=f"Document ingested with {len(chunk_texts)} chunk(s)",
    )


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    """Answer a question using the full RAG pipeline."""

    result = answer_question(
        question=request.question,
        top_k=request.top_k,
        category=request.category,
    )

    return QueryResponse(
        question=result["question"],
        answer=result["answer"],
        retrieved_chunks=[
            RetrievedChunk(
                title=chunk["title"],
                content=chunk["content"],
                score=chunk["score"],
            )
            for chunk in result["retrieved_chunks"]
        ],
        prompt_tokens=result["prompt_tokens"],
        completion_tokens=result["completion_tokens"],
        model=result["model"],
    )