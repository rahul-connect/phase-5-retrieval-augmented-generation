from rag.llm import stream_answer


def main() -> None:
    events = stream_answer(
        system_prompt="You are a helpful Python tutor.",
        user_prompt="Explain Python decorators in 3 short sentences.",
        max_tokens=200,
    )

    for event in events:
        if event["type"] == "delta":
            print(event["text"], end="", flush=True)

        elif event["type"] == "usage":
            print("\n\n--- Usage ---")
            print(f"Model: {event['model']}")
            print(f"Prompt tokens: {event['prompt_tokens']}")
            print(f"Completion tokens: {event['completion_tokens']}")


if __name__ == "__main__":
    main()