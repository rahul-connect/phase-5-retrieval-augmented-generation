from rag.models import Chunk


def reciprocal_rank_fusion(
    result_lists: list[list[tuple[Chunk, str, float]]],
    k: int = 60,
    top_k: int = 5,
) -> list[tuple[Chunk, str, float]]:

    scores: dict[int, tuple[Chunk, str, float]] = {}

    for result_list in result_lists:
        for rank, (chunk, title, _score) in enumerate(result_list):
            increment = 1.0 / (k + rank + 1)

            if chunk.id in scores:
                c, t, score = scores[chunk.id]
                scores[chunk.id] = (c, t, score + increment)
            else:
                scores[chunk.id] = (chunk, title, increment)

    return sorted(
        scores.values(),
        key=lambda x: x[2],
        reverse=True,
    )[:top_k]