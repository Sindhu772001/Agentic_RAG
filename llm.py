# app/rag/llm.py
from openai import AzureOpenAI
from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    LLM_DEPLOYMENT
)

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
)


def generate_answer(prompt: str) -> str:
    print("🤖 Sending prompt to LLM")

    response = client.chat.completions.create(
        model=LLM_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a helpful enterprise assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    answer = response.choices[0].message.content.strip()

    print("✅ LLM response received")
    return answer