from pathlib import Path
import os

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
import hashlib
import json


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 768


CACHE_FILE = Path("embedding_cache.json")


def make_cache_key(text: str) -> str:
    """Create a unique cache key for the text and embedding configuration."""

    content = f"{MODEL}:{EMBEDDING_DIMENSIONS}:{text}"

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def load_cache() -> dict[str, list[float]]:
    """Load previously generated embeddings from a JSON file."""

    if not CACHE_FILE.exists():
        return {}

    with CACHE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(cache: dict[str, list[float]]) -> None:
    """Save generated embeddings to a JSON file."""

    with CACHE_FILE.open("w", encoding="utf-8") as file:
        json.dump(cache, file)


def embed(
    text: str,
    cache: dict[str, list[float]],
) -> list[float]:
    """Generate an embedding or reuse a cached embedding."""

    key = make_cache_key(text)

    # Return an existing embedding without calling Gemini.
    if key in cache:
        return cache[key]

    # No cached embedding exists, so call Gemini.
    response = client.models.embed_content(
        model=MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )

    if not response.embeddings:
        raise ValueError("No embeddings returned")

    values = response.embeddings[0].values

    if values is None:
        raise ValueError("Embedding values are missing")

    vector = list(values)

    # Save the new embedding in memory.
    cache[key] = vector

    # Persist it immediately so interrupted runs retain progress.
    save_cache(cache)

    return vector


def embed_chunks(
    chunks: list[str],
    cache: dict[str, list[float]],
) -> list[list[float]]:
    """Generate or retrieve cached embeddings for every chunk."""

    embeddings = []

    for chunk in chunks:
        vector = embed(chunk, cache)
        embeddings.append(vector)

    return embeddings


def cosine_similarity(
    a: list[float],
    b: list[float],
) -> float:
    """Calculate cosine similarity between two vectors."""

    vector_a = np.array(a)
    vector_b = np.array(b)

    dot_product = np.dot(vector_a, vector_b)

    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Cannot compare zero-length vectors")

    return float(dot_product / (magnitude_a * magnitude_b))


def retrieve(
    query: str,
    chunks: list[str],
    vectors: list[list[float]],
    cache: dict[str, list[float]],
    top_k: int = 3,
) -> list[tuple[str, float]]:
    """Return the top-k most similar chunks for a query."""

    if len(chunks) != len(vectors):
        raise ValueError("Chunks and vectors must have matching lengths")

    query_vector = embed(query, cache)

    results = []

    for chunk, vector in zip(chunks, vectors):
        score = cosine_similarity(query_vector, vector)
        results.append((chunk, score))

    results.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return results[:top_k]



def chunk_fixed(text: str, chunk_size: int) -> list[str]:
    """Split text into fixed-size character chunks with no overlap."""

    chunks = []

    for start in range(0, len(text), chunk_size):
        chunks.append(text[start : start + chunk_size])

    return chunks


def chunk_fixed_with_overlap(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    """Split text into fixed-size chunks with overlap."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(text), step):
        chunk = text[start : start + chunk_size]

        if chunk:
            chunks.append(chunk)

        if start + chunk_size >= len(text):
            break

    return chunks


def chunk_recursive(
    text: str,
    chunk_size: int,
    separators: list[str] | None = None,
) -> list[str]:
    """Split text at natural boundaries, using smaller separators when needed."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if separators is None:
        separators = ["\n\n", "\n", ". ", " ", ""]

    # Base case: The text is already small enough.
    if len(text) <= chunk_size:
        return [text]

    # Choose the current separator.
    separator = separators[0]

    # Keep the remaining separators for recursive calls.
    remaining_separators = separators[1:]

    # Last resort: Split directly by character count.
    if separator == "":
        chunks = []

        for start in range(0, len(text), chunk_size):
            chunk = text[start : start + chunk_size]
            chunks.append(chunk)

        return chunks

    # Split text using the current separator.
    parts = text.split(separator)

    chunks: list[str] = []
    current = ""

    for part in parts:

        # Try combining the current chunk with the next part.
        candidate = current + separator + part if current else part

        if len(candidate) <= chunk_size:
            # The combined text fits.
            current = candidate

        else:
            # Save the current chunk before starting another.
            if current:
                chunks.append(current)

            # If the individual part is too large,
            # split it again using smaller separators.
            if len(part) > chunk_size:
                smaller_chunks = chunk_recursive(
                    part,
                    chunk_size,
                    remaining_separators,
                )

                chunks.extend(smaller_chunks)

                current = ""

            else:
                # The part fits by itself.
                current = part

    # Save the final chunk if it contains text.
    if current:
        chunks.append(current)

    return chunks


def preview(text: str, max_length: int = 120) -> str:
    """Return a shortened single-line preview of a chunk."""

    cleaned = text.replace("\n", " ")

    return cleaned[:max_length]


def compare_strategies(
    document: str,
    chunk_size: int,
    overlap: int,
    cache: dict[str, list[float]],
) -> None:
    """Compare semantic retrieval across three chunking strategies."""

    strategies = {
        "fixed_no_overlap": chunk_fixed(document, chunk_size),

        "fixed_with_overlap": chunk_fixed_with_overlap(
            document,
            chunk_size,
            overlap,
        ),

        "recursive": chunk_recursive(document, chunk_size),
    }

    queries = [
        "How many vacation days do I get?",
        "What's the policy on working from home?",
        "How do I report harassment?",
        "What's the budget for professional development?",
    ]

    print(f"\n{'#' * 70}")
    print(f"CHUNK SIZE: {chunk_size} | OVERLAP: {overlap}")
    print(f"{'#' * 70}")

    for name, chunks in strategies.items():

        print(f"\n{'=' * 70}")
        print(f"Strategy: {name}")
        print(f"Total chunks: {len(chunks)}")
        print(f"{'=' * 70}")

        vectors = embed_chunks(chunks, cache)

        for query in queries:

            results = retrieve(
                query=query,
                chunks=chunks,
                vectors=vectors,
                cache=cache,
                top_k=3,
            )

            print(f"\nQuestion: {query}")

            for rank, (chunk, score) in enumerate(results, start=1):

                print(
                    f"Rank {rank} | "
                    f"Similarity: {score:.4f} | "
                    f"{preview(chunk)}"
                )

            # Show the complete top-ranked chunk.
            if results:
                print("\nComplete top-1 chunk:")
                print(results[0][0])

            print("-" * 70)



def main() -> None:
    """Compare chunking strategies across three chunk sizes."""

    document = Path("handbook.txt").read_text(encoding="utf-8")

    cache = load_cache()

    experiments = [
        (300, 60),
        # (600, 120),
        # (1500, 300),
    ]

    for chunk_size, overlap in experiments:

        compare_strategies(
            document=document,
            chunk_size=chunk_size,
            overlap=overlap,
            cache=cache,
        )

    print("\nAll experiments completed.")
    print(f"Total cached embeddings: {len(cache)}")



if __name__ == "__main__":
    main()





# def main() -> None:
#     """Load the employee handbook and inspect its contents."""

#     document = Path("handbook.txt").read_text(encoding="utf-8")

#     chunk_size = 1500
#     overlap = 300

#     strategies = {
#         "fixed_no_overlap": chunk_fixed(document, chunk_size),

#         "fixed_with_overlap": chunk_fixed_with_overlap(
#             document,
#             chunk_size,
#             overlap,
#         ),

#         "recursive": chunk_recursive(document, chunk_size),
#     }

#     print("=" * 70)
#     print("Chunk Statistics")
#     print("=" * 70)

#     for name, chunks in strategies.items():

#         sizes = [len(chunk) for chunk in chunks]

#         print(
#             f"{name:20s} "
#             f"count={len(chunks):2d} "
#             f"min={min(sizes):4d} "
#             f"max={max(sizes):4d} "
#             f"avg={sum(sizes) // len(sizes):4d}"
#         )