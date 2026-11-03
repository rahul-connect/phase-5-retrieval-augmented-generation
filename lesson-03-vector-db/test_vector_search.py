
"""Practice vector similarity search using pgvector."""

from rag.database import SessionLocal
from rag.repository import search_similar_chunks


def main() -> None:
    """Search stored chunks using a dummy vector."""

    query_embedding = [0.0] * 767 + [1.0]

    with SessionLocal() as db:
        results = search_similar_chunks(
            db=db,
            query_embedding=query_embedding,
            top_k=5,
        )

        for chunk, title, distance in results:
            similarity = 1 - distance

            print(f"Document: {title}")
            print(f"Chunk: {chunk.content}")
            print(f"Cosine distance: {distance:.4f}")
            print(f"Cosine similarity: {similarity:.4f}")
            print("-" * 30)


if __name__ == "__main__":
    main()
