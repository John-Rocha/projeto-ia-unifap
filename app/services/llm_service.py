from openai import OpenAI
from app.core.config import settings

_client = OpenAI(api_key=settings.openai_api_key)


def generate(prompt: str) -> str:
    resp = _client.chat.completions.create(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
