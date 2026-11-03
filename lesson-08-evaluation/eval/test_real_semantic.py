from rag.search import search
from eval.retrieval_metrics import (
    summarize_retrieval_results,
    evaluate_retrieval_case,
)


#query = "What is REST API?"
query = "Compare REST and GraphQL"

results = search(query, top_k=5)

print("\nTop retrieved chunk:")
print(results[0]["title"])
print(results[0]["content"])

summary = summarize_retrieval_results(results)

print("Query:", query)

for rank, result in enumerate(results, start=1):
    print(
        f"{rank}. {result['title']} "
        f"(similarity={result['similarity']:.3f})"
    )

print("Summary:", summary)

#relevant_titles = ["REST API Design Principles"]
relevant_titles = [
    "REST API Design Principles",
    "What is GraphQL",
]

metrics = evaluate_retrieval_case(
    retrieved_titles=summary["document_titles"],
    relevant_titles=relevant_titles,
    k=5,
)

print("Metrics:", metrics)

for k in [1, 3, 5]:
    metrics = evaluate_retrieval_case(
        retrieved_titles=summary["document_titles"],
        relevant_titles=relevant_titles,
        k=k,
    )

    print(f"K={k}: {metrics}")