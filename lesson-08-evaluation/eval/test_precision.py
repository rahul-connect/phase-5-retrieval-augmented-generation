from eval.retrieval_metrics import precision_at_k


# Test 1: All retrieved documents are relevant
print(precision_at_k(
    ["REST", "GraphQL", "Python"],
    ["REST", "GraphQL"],
    k=2,
))

# Test 2: One relevant document among three
print(precision_at_k(
    ["REST", "Database", "Python"],
    ["REST", "GraphQL"],
    k=3,
))

# Test 3: No documents retrieved
print(precision_at_k(
    [],
    ["REST", "GraphQL"],
    k=3,
))