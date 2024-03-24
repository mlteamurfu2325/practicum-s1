"""Module for fetching summary from LLM API for provided text."""

from os import getenv

from openai import OpenAI


def fetch_summary(
    text: str,
    llm_model: str = "openai/gpt-4-turbo-preview",
    llm_api_key: str | None = None,
) -> str:
    """Fetch summary from LLM API using given text and optionally an API key.

    Args:
        text: Input text to summarize.
        llm_model: Name of LLM model to use. Defaults to "openai/gpt-4-turbo-preview".
        llm_api_key: API key for service. Defaults to None.

    Returns:
        Summary text response from API.

    Example:
        >>> summary = fetch_summary(text)
        >>> summary = fetch_summary(text, llm_api_key=api_key)
    """
    prompt = (
        "Дай краткий пересказ этого текста на русском языке. "
        "В твоём ответе должен быть только сам пересказ. "
        "Не используй ничего, кроме самого текста, который я тебе "
        f"сейчас отправил после двоеточия: {text}"
    )

    llm_api_key = llm_api_key or getenv("LLM_API_KEY")
    llm_url = getenv("LLM_URL")

    client = OpenAI(base_url=llm_url, api_key=llm_api_key)

    completion = client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=int(len(prompt) * 1.5),
    )

    response = completion.choices[0].message.content
    return response
