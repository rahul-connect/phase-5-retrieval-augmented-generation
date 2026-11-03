from rag.query_preprocessing import prepare_keyword_query


queries = [
    "Compare REST and GraphQL",
    "Compare PostgreSQL vs SQLite",
    "Compare Python versus JavaScript",
    "Compare C++ and Java",
    "Compare FastAPI and Django REST Framework",
    'Compare "REST" and GraphQL OR Python',
    "What is RAG?",
]

for query in queries:
    prepared = prepare_keyword_query(query)
    print(f"{query} -> {prepared}")