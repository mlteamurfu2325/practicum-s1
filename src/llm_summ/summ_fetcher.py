import openai


def fetch_summary(key: str, text: str) -> str:
    openai.api_key = key
    openai.base_url = "https://api.vsegpt.ru:6070/v1/"

    prompt = f"Дай краткий пересказ этого текста: {text}"

    messages = []

    messages.append({"role": "user", "content": prompt})

    response_big = openai.chat.completions.create(
        model="fireworks/mixtral-8x7b-fw-chat",
        messages=messages,
        temperature=0.7,
        n=1,
        max_tokens=int(len(prompt) * 1.5),
    )

    response = response_big.choices[0].message.content

    return response
