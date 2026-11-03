from eval.retrieval_metrics import recall_at_k


# Case 1: Partial retrieval
print(recall_at_k(
    retrieved_titles=["REST", "Database", "Python"],
    relevant_titles=["REST", "GraphQL"],
    k=3,
))

# Case 2: Perfect retrieval
print(recall_at_k(
    retrieved_titles=["REST", "GraphQL", "Python"],
    relevant_titles=["REST", "GraphQL"],
    k=3,
))

# Case 3: Out-of-corpus query
print(recall_at_k(
    retrieved_titles=["REST", "Python"],
    relevant_titles=[],
    k=2,
))