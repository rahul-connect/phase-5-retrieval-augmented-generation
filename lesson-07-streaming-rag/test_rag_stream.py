from rag.rag_pipeline import stream_answer_pipeline


def main() -> None:
    events = stream_answer_pipeline(
        question="What is Retrieval-Augmented Generation?",
        top_k=3,
        category="programming",
    )

    for event in events:
        if event["type"] == "chunks":
            print("\n--- Retrieved Sources ---")

            for chunk in event["chunks"]:
                print(f"Title: {chunk['title']}")
                print(f"Score: {chunk['score']:.3f}")

            print("\n--- Streaming Answer ---")

        elif event["type"] == "delta":
            print(event["text"], end="", flush=True)

        elif event["type"] == "usage":
            print("\n\n--- Usage ---")
            print(f"Prompt tokens: {event['prompt_tokens']}")
            print(f"Completion tokens: {event['completion_tokens']}")
            print(f"Model: {event['model']}")


if __name__ == "__main__":
    main()