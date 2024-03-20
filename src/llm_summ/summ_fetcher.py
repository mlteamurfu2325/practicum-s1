"""Module for fetching summary from LLM API for provided text."""
from os import getenv

from openai import OpenAI


def fetch_summary(
    text: str,
    llm_model: str = "openai/gpt-4-turbo-preview",
    llm_api_key: str | None = None,
) -> str:
    """Fetch summary from LLM API using given text and optionally an API key.

    :param text: Input text to summarize
    :type text: str
    :param llm_model: Name of LLM model to use
    :type llm_model: str
    :param llm_api_key: API key for service (optional)
    :type llm_api_key: str, optional
    :return: Summary text response from API
    :rtype: str

    :Example:

    >>> summary = fetch_summary(text)
    >>> summary = fetch_summary(api_key, text)

    """

    prompt = f"Дай краткий пересказ этого текста на русском языке. В твоём ответе должен быть только сам пересказ. Не используй ничего, кроме самого текста, который я тебе сейчас отправил после двоеточия: {text}"

    client = OpenAI(
        base_url=getenv("LLM_URL"),
        api_key=getenv("LLM_API_KEY"),
    )

    completion = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            },
        ],
        temperature=0.7,
        max_tokens=int(len(prompt) * 1.5),
    )

    response = completion.choices[0].message.content

    return response
