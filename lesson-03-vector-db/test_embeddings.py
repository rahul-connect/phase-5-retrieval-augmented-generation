"""Test Gemini embedding generation and caching."""

from rag.embeddings import embed_text


def main() -> None:
    """Generate an embedding and display its dimensions."""

    text = "Python supports functions and classes."

    embedding = embed_text(
        text=text,
        task_type="RETRIEVAL_DOCUMENT",
    )

    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First five values: {embedding[:5]}")


if __name__ == "__main__":
    main()