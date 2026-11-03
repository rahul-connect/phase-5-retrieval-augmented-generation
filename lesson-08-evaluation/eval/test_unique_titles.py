from eval.retrieval_metrics import unique_document_titles


results = [
    {"title": "REST", "content": "Chunk 1"},
    {"title": "REST", "content": "Chunk 2"},
    {"title": "GraphQL", "content": "Chunk 1"},
    {"title": "Python", "content": "Chunk 1"},
]

titles = unique_document_titles(results)

print(titles)
print(len(titles))