
"""Generate and cache text embeddings using Gemini."""

from google import genai
from google.genai import types

from rag.config import get_settings
from rag.embedding_cache import load_cache, make_cache_key, save_cache
from rag.models import EMBEDDING_DIM


EMBEDDING_MODEL = "gemini-embedding-001"

settings = get_settings()
client = genai.Client(api_key=settings.google_api_key)


def embed_text(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT",
) -> list[float]:
    """Generate or retrieve a cached text embedding."""

    cache_key = make_cache_key(
        text=text,
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIM,
        task_type=task_type,
    )

    cache = load_cache()

    if cache_key in cache:
        print("CACHE HIT: Returning saved embedding")
        return cache[cache_key]

    print("CACHE MISS: Requesting embedding from Gemini")

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIM,
            task_type=task_type,
        ),
    )

    if not response.embeddings or response.embeddings[0].values is None:
        raise ValueError("Gemini returned no embedding values.")

    embedding = list(response.embeddings[0].values)

    cache[cache_key] = embedding
    save_cache(cache)

    return embedding
