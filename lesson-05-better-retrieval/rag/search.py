from rag.database import SessionLocal
from rag.embeddings import embed_text
from rag.repository import search_similar_chunks

def search(query: str, top_k: int = 5) -> list[dict]:
    """Find the most semantically similar document chunks."""

    query_vector = embed_text(
        query,
        task_type="RETRIEVAL_QUERY",
    )

    with SessionLocal() as db:
        rows = search_similar_chunks(
            db=db,
            query_embedding=query_vector,
            top_k=top_k,
        )

        results = []

        for chunk, title, distance in rows:
            similarity = 1 - distance

            results.append({
                "title": title,
                "content": chunk.content,
                "similarity": similarity,
            })

        return results


def main() -> None:
    queries = [
        "How do I make bread rise without commercial yeast?",
        "What's the best way to design a REST API?",
        "Tell me about Python concurrency",
        "How do planets form mountains?",
        "What should I see when I visit Japan?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")

        results = search(query, top_k=3)
        for index, result in enumerate(results, start=1):
            print(
                f"{index}. {result['title']} "
                f"(similarity: {result['similarity']:.4f})"
            )


if __name__ == "__main__":
    main()