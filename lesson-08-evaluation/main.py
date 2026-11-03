"""FastAPI application entry point."""

from fastapi import FastAPI

from rag.exceptions import register_exception_handlers
from rag.routes import router


app = FastAPI(
    title="RAG API",
    description="RAG service for querying a knowledge base",
    version="0.1.0",
)

register_exception_handlers(app)

app.include_router(router)