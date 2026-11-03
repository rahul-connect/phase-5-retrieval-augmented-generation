"""LLM provider wrapper using Groq."""

from groq import Groq

from rag.config import get_settings

settings = get_settings()

client = Groq(api_key=settings.groq_api_key)


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