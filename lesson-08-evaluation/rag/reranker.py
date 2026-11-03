import httpx

from rag.config import get_settings

settings = get_settings()


def rerank(
    query: str,
    candidates: list[tuple],
    top_k: int = 5,
) -> list[tuple]:

    if not candidates:
        return []

    documents = [
        chunk.content
        for chunk, _title, _score in candidates
    ]

    payload = {
        "model": settings.jina_model,
        "query": query,
        "documents": documents,
        "top_n": top_k,
    }

    headers = {
        "Authorization": f"Bearer {settings.jina_api_key}",
        "Content-Type": "application/json",
    }

    response = httpx.post(
        settings.jina_url,
        headers=headers,
        json=payload,
        timeout=30.0,
    )

    response.raise_for_status()
    data = response.json()

    reranked = []

    for item in data["results"]:
        original_index = item["index"]
        score = item["relevance_score"]

        chunk, title, _old_score = candidates[original_index]
        reranked.append((chunk, title, float(score)))

    return reranked