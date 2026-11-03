import os

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------

load_dotenv()

api_key = os.environ["GOOGLE_API_KEY"]

client = genai.Client(api_key=api_key)

MODEL = "gemini-embedding-001"


# ---------------------------------------------------------------
# Helper Function 1: Generate Embeddings
# ---------------------------------------------------------------

def embed(text: str) -> list[float]:
    """Generate an embedding vector for the given text."""

    result = client.models.embed_content(
        model=MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768,
        ),
    )

    # Check whether the API returned any embeddings.
    if not result.embeddings:
        raise ValueError("The API returned no embeddings.")

    # Extract the numerical values from the first embedding.
    vector = result.embeddings[0].values

    # Check whether the embedding contains numerical values.
    if vector is None:
        raise ValueError("The embedding contains no values.")

    return vector


# ---------------------------------------------------------------
# Helper Function 2: Calculate Cosine Similarity
# ---------------------------------------------------------------

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two embedding vectors."""

    a_arr = np.array(a)
    b_arr = np.array(b)

    return float(
        np.dot(a_arr, b_arr)
        / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr))
    )


# ---------------------------------------------------------------
# Main Function: Run All Four Experiments
# ---------------------------------------------------------------

def main() -> None:
    """Explore embeddings through four experiments."""

    # ===============================================================
    # Experiment A: What does an embedding actually look like?
    # ===============================================================

    text = "How do I reset my password?"
    vector = embed(text)

    print("=" * 60)
    print("Experiment A — The shape of an embedding")
    print("=" * 60)

    print(f"Text: {text!r}")
    print(f"Vector length: {len(vector)} dimensions")
    print(f"First 5 values: {vector[:5]}")
    print(f"Last 5 values: {vector[-5:]}")
    print(f"Min value: {min(vector):.4f}")
    print(f"Max value: {max(vector):.4f}")

    # ===============================================================
    # Experiment B: Similar meanings should be close
    # ===============================================================

    print("\n" + "=" * 60)
    print("Experiment B — Similar vs. different meanings")
    print("=" * 60)

    query = "How do I reset my password?"

    candidates = [
        "I forgot my login credentials.",
        "Steps to recover your account.",
        "The weather is nice today.",
        "How do I change my shipping address?",
        "Password reset instructions.",
    ]

    # Generate the query embedding once.
    query_vector = embed(query)

    # Store each candidate alongside its similarity score.
    results = []

    for candidate in candidates:
        # Generate the candidate's embedding.
        candidate_vector = embed(candidate)

        # Compare the candidate embedding with the query embedding.
        similarity = cosine_similarity(
            query_vector,
            candidate_vector,
        )

        # Store the sentence and its similarity score as a tuple.
        results.append((candidate, similarity))

    # Sort by similarity score, highest first.
    results.sort(key=lambda x: x[1], reverse=True)

    print(f"Query: {query!r}")
    print()
    print(f"{'Candidate':<50} Similarity")
    print("-" * 65)

    for candidate, similarity in results:
        print(f"{candidate:<50} {similarity:.4f}")

    # ===============================================================
    # Experiment C: The same text produces the same embedding
    # ===============================================================

    print("\n" + "=" * 60)
    print("Experiment C — Determinism check")
    print("=" * 60)

    text = "Hello world"

    # Generate two embeddings for exactly the same text.
    v1 = embed(text)
    v2 = embed(text)

    # Compare their directions.
    similarity = cosine_similarity(v1, v2)

    print(f"Same text, embedded twice. Similarity: {similarity:.6f}")
    print("(Expected: very close to 1.0)")

    # Check whether every corresponding value is identical.
    print(f"Exactly identical vectors: {v1 == v2}")

    # ===============================================================
    # Experiment D: Small rewording vs. meaning changes
    # ===============================================================

    print("\n" + "=" * 60)
    print("Experiment D — Small rewording vs. true synonyms")
    print("=" * 60)

    base = "The cat sat on the mat."

    variants = [
        "The cat sat on the mat.",
        "The cat sat on the mat",
        "the cat sat on the mat.",
        "A cat is sitting on the mat.",
        "The dog sat on the mat.",
        "The mat sat on the cat.",
    ]

    # Generate the base embedding once.
    base_vector = embed(base)

    print(f"Base: {base!r}")
    print()
    print(f"{'Variant':<45} Similarity")
    print("-" * 60)

    for variant in variants:
        # Generate an embedding for the current variant.
        v = embed(variant)

        # Compare the variant with the original sentence.
        similarity = cosine_similarity(base_vector, v)

        print(f"{variant!r:<45} {similarity:.4f}")


# ---------------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------------

if __name__ == "__main__":
    main()