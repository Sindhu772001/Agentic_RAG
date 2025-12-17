# app/rag/embeddings.py
from openai import AzureOpenAI
from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    EMBEDDING_DEPLOYMENT
)

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
)

def embed_chunks(chunks, batch_size=16):
    print("🧬 Starting embedding generation")
    embedded = []

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["content"] for c in batch]

        print(
            f"➡️ Embedding batch {i//batch_size + 1} "
            f"| size={len(texts)}"
        )

        response = client.embeddings.create(
            model=EMBEDDING_DEPLOYMENT,
            input=texts
        )

        for idx, emb in enumerate(response.data):
            embedded.append({
                "embedding": emb.embedding,
                "content": batch[idx]["content"],
                "metadata": batch[idx]["metadata"]
            })

    print(f"✅ Embeddings created: {len(embedded)}")
    return embedded


def embed_query(query: str):
    """
    Embed a single query using the same embedding model.
    """
    print("🧬 Creating embedding for query")

    response = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=[query]
    )

    return response.data[0].embedding