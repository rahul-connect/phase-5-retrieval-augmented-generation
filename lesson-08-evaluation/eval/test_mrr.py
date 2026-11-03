from eval.retrieval_metrics import mean_reciprocal_rank


results = [
    (["REST", "Python"], ["REST"]),
    (["Python", "GraphQL"], ["GraphQL"]),
    (["Database", "Python"], ["REST"]),
]

print(mean_reciprocal_rank(results))

# Empty evaluation dataset
print(mean_reciprocal_rank([]))