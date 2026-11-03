"""Practice generating stable embedding cache keys."""

from rag.embedding_cache import make_cache_key


def main() -> None:
    """Compare cache keys for identical and different requests."""

    key1 = make_cache_key(
        text="What is Python?",
        model="gemini-embedding-001",
        dimensions=768,
        task_type="RETRIEVAL_QUERY",
    )

    key2 = make_cache_key(
        text="What is Python?",
        model="gemini-embedding-001",
        dimensions=768,
        task_type="RETRIEVAL_QUERY",
    )

    key3 = make_cache_key(
        text="What is Python?",
        model="gemini-embedding-001",
        dimensions=768,
        task_type="RETRIEVAL_DOCUMENT",
    )

    print("Same request:", key1 == key2)
    print("Different task type:", key1 == key3)


if __name__ == "__main__":
    main()