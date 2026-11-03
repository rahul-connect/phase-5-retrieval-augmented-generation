from eval.retrieval_metrics import evaluate_retrieval_case


result = evaluate_retrieval_case(
    retrieved_titles=["Python", "REST", "GraphQL"],
    relevant_titles=["REST", "GraphQL"],
    k=2,
)

print(result)