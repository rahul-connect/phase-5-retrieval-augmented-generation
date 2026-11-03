"""LLM provider wrapper using Groq."""

from groq import Groq
from collections.abc import Iterator

from rag.config import get_settings

settings = get_settings()

client = Groq(api_key=settings.groq_api_key)


def stream_answer(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 1024,
) -> Iterator[dict]:
    """Stream generated text followed by usage metadata."""

    stream = client.chat.completions.create(
        model=settings.groq_model_name,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )

    model_name = settings.groq_model_name
    prompt_tokens = 0
    completion_tokens = 0

    for chunk in stream:
        if chunk.model:
            model_name = chunk.model

        if chunk.choices:
            delta = chunk.choices[0].delta.content

            if delta:
                yield {
                    "type": "delta",
                    "text": delta,
                }

        x_groq = getattr(chunk, "x_groq", None)

        if x_groq is not None and x_groq.usage is not None:
            prompt_tokens = x_groq.usage.prompt_tokens
            completion_tokens = x_groq.usage.completion_tokens

    yield {
        "type": "usage",
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "model": model_name,
    }


def generate_answer(
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1024
) -> dict:

    response = client.chat.completions.create(
        model=settings.groq_model_name,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content

    if content is None:
        raise RuntimeError("LLM returned no content")

    usage = response.usage

    if usage is None:
        raise RuntimeError("LLM returned no usage information")

    return {
        "answer": content,
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "model": response.model,
    }