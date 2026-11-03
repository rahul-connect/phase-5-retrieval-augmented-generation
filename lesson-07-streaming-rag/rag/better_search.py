from rag.database import SessionLocal
from rag.embeddings import embed_text
from rag.fusion import reciprocal_rank_fusion
from rag.repository import (
    keyword_search,
    search_similar_chunks_with_filter,
)

from rag.reranker import rerank


def _format_results(rows: list) -> list[dict]:
    return [
        {
            "title": title,
            "content": chunk.content,
            "score": score,
        }
        for chunk, title, score in rows
    ]


def semantic_only(
    query: str,
    top_k: int = 5,
    category: str | None = None,
) -> list[dict]:

    vector = embed_text(query, task_type="RETRIEVAL_QUERY")

    with SessionLocal() as db:
        rows = search_similar_chunks_with_filter(
            db=db,
            query_embedding=vector,
            top_k=top_k,
            category=category,
        )

    return _format_results(rows)


def keyword_only(
    query: str,
    top_k: int = 5,
    category: str | None = None,
) -> list[dict]:

    with SessionLocal() as db:
        rows = keyword_search(
            db=db,
            query=query,
            category=category,
            top_k=top_k,
        )

    return _format_results(rows)


def hybrid(
    query: str,
    top_k: int = 5,
    category: str | None = None,
) -> list[dict]:
    vector = embed_text(query, task_type="RETRIEVAL_QUERY")

    with SessionLocal() as db:
        semantic_rows = search_similar_chunks_with_filter(
            db=db,
            query_embedding=vector,
            top_k=20,
            category=category,
        )

        keyword_rows = keyword_search(
            db=db,
            query=query,
            top_k=20,
            category=category,
        )

    fused_rows = reciprocal_rank_fusion(
        [semantic_rows, keyword_rows],
        top_k=top_k,
    )

    return _format_results(fused_rows)




def hybrid_reranked(
    query: str,
    top_k: int = 5,
    category: str | None = None,
) -> list[dict]:

    vector = embed_text(query, task_type="RETRIEVAL_QUERY")

    with SessionLocal() as db:
        semantic_rows = search_similar_chunks_with_filter(
                db=db,
                query_embedding=vector,
                top_k=20,
                category=category,
        )

        keyword_rows = keyword_search(
                db=db,
                query=query,
                top_k=20,
                category=category,
        )

    candidates = reciprocal_rank_fusion(
        [semantic_rows, keyword_rows],
        top_k=10,
    )

    reranked_rows = rerank(
        query=query,
        candidates=candidates,
        top_k=top_k,
    )

    return _format_results(reranked_rows)
    