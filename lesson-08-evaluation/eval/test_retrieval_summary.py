from eval.retrieval_metrics import summarize_retrieval_results


results = [
    {"title": "REST", "content": "Chunk 1"},
    {"title": "REST", "content": "Chunk 2"},
    {"title": "GraphQL", "content": "Chunk 1"},
]

summary = summarize_retrieval_results(results)

print(summary)