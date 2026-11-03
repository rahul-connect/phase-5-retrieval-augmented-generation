"""Local JSON cache for text embeddings."""

import json
from pathlib import Path
import hashlib

CACHE_PATH = Path("embedding_cache.json")


def make_cache_key(
    text: str,
    model: str,
    dimensions: int,
    task_type: str,
) -> str:
    """Generate a stable cache key for an embedding request."""

    cache_input = f"{model}:{dimensions}:{task_type}:{text}"

    return hashlib.sha256(
        cache_input.encode("utf-8")
    ).hexdigest()


def load_cache() -> dict[str, list[float]]:
    """Load cached embeddings from disk."""

    if not CACHE_PATH.exists():
        return {}

    with CACHE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(cache: dict[str, list[float]]) -> None:
    """Save cached embeddings to disk."""

    with CACHE_PATH.open("w", encoding="utf-8") as file:
        json.dump(cache, file)