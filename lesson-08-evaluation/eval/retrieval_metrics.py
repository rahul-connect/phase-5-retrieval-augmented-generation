"""Deterministic retrieval evaluation metrics."""


def recall_at_k(
    retrieved_titles: list[str],
    relevant_titles: list[str],
    k: int,
) -> float | None:
    """Calculate recall at K, or None when recall is undefined."""

    if not relevant_titles:
        return None

    top_k = retrieved_titles[:k]

    retrieved_set = set(top_k)
    relevant_set = set(relevant_titles)

    hits = retrieved_set & relevant_set

    return len(hits) / len(relevant_set)


def precision_at_k(
    retrieved_titles: list[str],
    relevant_titles: list[str],
    k: int,
) -> float:
    """Calculate the fraction of retrieved documents that are relevant."""

    top_k = retrieved_titles[:k]

    if not top_k:
        return 0.0

    relevant_set = set(relevant_titles)

    hits = sum(
        1 for title in top_k
        if title in relevant_set
    )

    return hits / len(top_k)


def reciprocal_rank(
    retrieved_titles: list[str],
    relevant_titles: list[str],
) -> float:
    """Return the reciprocal rank of the first relevant document."""

    relevant_set = set(relevant_titles)

    for position, title in enumerate(retrieved_titles, start=1):
        if title in relevant_set:
            return 1.0 / position

    return 0.0


def mean_reciprocal_rank(
    results: list[tuple[list[str], list[str]]],
) -> float:
    """Calculate MRR across multiple in-corpus queries."""

    if not results:
        return 0.0

    total_rr = 0.0

    for retrieved_titles, relevant_titles in results:
        rr = reciprocal_rank(retrieved_titles, relevant_titles)
        total_rr += rr

    return total_rr / len(results)



def evaluate_retrieval_case(
    retrieved_titles: list[str],
    relevant_titles: list[str],
    k: int,
) -> dict:
    """Evaluate one retrieval result at K."""

    return {
        "recall": recall_at_k(
            retrieved_titles, relevant_titles, k
        ),
        "precision": precision_at_k(
            retrieved_titles, relevant_titles, k
        ),
        "reciprocal_rank": reciprocal_rank(
            retrieved_titles[:k], relevant_titles
        ),
    }


def unique_document_titles(
    results: list[dict],
) -> list[str]:
    """Extract unique document titles in retrieval order."""

    titles = []
    seen = set()

    for result in results:
        title = result["title"]

        if title not in seen:
            titles.append(title)
            seen.add(title)

    return titles


def summarize_retrieval_results(
    results: list[dict],
) -> dict:
    """Summarize chunk and document counts."""

    unique_titles = unique_document_titles(results)

    return {
        "chunk_count": len(results),
        "document_count": len(unique_titles),
        "document_titles": unique_titles,
    }