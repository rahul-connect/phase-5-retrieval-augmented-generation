"""Run questions through the RAG pipeline."""

from rag.rag_pipeline import answer_question


def display_result(result: dict) -> None:
    """Display the result of a RAG question."""

    print(f"\nQuestion: {result['question']}")
    print(f"\nAnswer: {result['answer']}")

    print("\nRetrieved chunks:")

    for index, chunk in enumerate(result["retrieved_chunks"], start=1):
        print(
            f"{index}. {chunk['title']} "
            f"(similarity: {chunk['similarity']:.4f})"
        )

        preview = chunk["content"][:120].replace("\n", " ")
        print(f"    {preview}...")

    print("\nUsage:")
    print(f"Model: {result['model']}")
    print(f"Prompt tokens: {result['prompt_tokens']}")
    print(f"Completion tokens: {result['completion_tokens']}")


def main() -> None:
    questions = [
        "How do I make bread without commercial yeast?",
        "What are the principles behind REST API design?",
        "How does Python's async/await work?",
        "What should I know about visiting Kyoto?",
        "How are mountains formed and what happens when tectonic plates collide?",
        "What's the capital of France?",
        "How do I file my US taxes?",
    ]

    for question in questions:
        result = answer_question(question, top_k=3)
        display_result(result)


if __name__ == "__main__":
    main()