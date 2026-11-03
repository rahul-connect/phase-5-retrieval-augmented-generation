from eval.retrieval_metrics import reciprocal_rank


# Test 1: First relevant document at rank 1
print(reciprocal_rank(
    ["REST", "Python", "Database"],
    ["REST", "GraphQL"],
))

# Test 2: First relevant document at rank 2
print(reciprocal_rank(
    ["Python", "REST", "GraphQL"],
    ["REST", "GraphQL"],
))

# Test 3: First relevant document at rank 3
print(reciprocal_rank(
    ["Python", "Database", "REST"],
    ["REST"],
))

# Test 4: No relevant document retrieved
print(reciprocal_rank(
    ["Python", "Database", "Vaccines"],
    ["REST", "GraphQL"],
))