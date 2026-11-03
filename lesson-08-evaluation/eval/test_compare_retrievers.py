from rag.search import search
from rag.better_search import hybrid, hybrid_reranked

from eval.retrieval_metrics import (
    evaluate_retrieval_case,
    unique_document_titles,
)

query = "Compare REST and GraphQL"

relevant_titles = [
    "REST API Design Principles",
    "What is GraphQL",
]

top_k = 5

strategies = {
    "Semantic": search,
    "Hybrid": hybrid,
    "Hybrid + Reranking": hybrid_reranked,
}

for name, retriever in strategies.items():
    results = retriever(query, top_k=top_k)

    retrieved_titles = unique_document_titles(results)

    metrics = evaluate_retrieval_case(
        retrieved_titles=retrieved_titles,
        relevant_titles=relevant_titles,
        k=top_k,
    )

    print(f"\n{name}")
    print("Retrieved:", retrieved_titles)
    print("Metrics:", metrics)