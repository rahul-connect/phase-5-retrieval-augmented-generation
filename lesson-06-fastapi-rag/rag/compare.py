
"""Compare retrieval strategies against a fixed set of queries."""

from rag.better_search import (
    semantic_only,
    keyword_only,
    hybrid,
    hybrid_reranked,
)


def display(name: str, results: list[dict]) -> None:
    """Print the ranked results for one retrieval strategy."""
    print(f"\n  {name}")

    for i, result in enumerate(results, start=1):
        preview = result["content"][:80].replace("\n", " ")

        print(
            f"    [{i}] score={result['score']:.4f}  "
            f"{result['title']}"
        )
        print(f"        {preview}...")


def compare_query(query: str, category: str | None = None) -> None:
    """Run all four retrieval strategies for the same query."""
    print("\n" + "=" * 80)
    print(f"Query: {query!r}")

    if category is not None:
        print(f"Filter: category={category}")

    print("=" * 80)

    display(
        "semantic_only",
        semantic_only(query, top_k=3, category=category),
    )

    display(
        "keyword_only",
        keyword_only(query, top_k=3, category=category),
    )

    display(
        "hybrid",
        hybrid(query, top_k=3, category=category),
    )

    display(
        "hybrid_reranked",
        hybrid_reranked(query, top_k=3, category=category),
    )


def main() -> None:
    """Compare retrieval methods with and without metadata filters."""
    queries_no_filter = [
        "How do I make bread without commercial yeast?",
        "What are the principles behind REST API design?",
        "How are mountains formed?",
        "Tell me about Python concurrency",
    ]

    for query in queries_no_filter:
        compare_query(query)

    print("\n\n" + "#" * 80)
    print("# Now with metadata filters")
    print("#" * 80)

    compare_query("How do I prepare dough?", category="cooking")
    compare_query("Tell me about async programming", category="programming")


if __name__ == "__main__":
    main()
