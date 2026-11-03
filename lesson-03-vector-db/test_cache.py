"""Practice saving and loading an embedding cache."""

from rag.embedding_cache import load_cache, save_cache


def main() -> None:
    """Save a dummy embedding and read it back."""

    cache = load_cache()

    cache["practice-key"] = [0.1, 0.2, 0.3]

    save_cache(cache)

    loaded_cache = load_cache()

    print(loaded_cache["practice-key"])


if __name__ == "__main__":
    main()