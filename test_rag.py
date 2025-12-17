# test_rag.py

from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    LLM_DEPLOYMENT
)
from app.rag.vectorstore import get_vectorstore
from app.rag.embeddings import embed_query
from app.rag.retriever import retrieve
from app.rag.prompt import RAG_PROMPT

from openai import AzureOpenAI


def build_context(chunks):
    """
    Build context text for LLM from retrieved chunks.
    """
    print("\n🧠 Building context for LLM")

    context_blocks = []

    for idx, chunk in enumerate(chunks, start=1):
        meta = chunk["metadata"]

        block = f"""
[Chunk {idx}]
Source: {meta.get('source')}
Page: {meta.get('page')}
Type: {meta.get('type')}
Distance Score: {chunk['score']:.4f}

Content:
{chunk['content']}
"""
        context_blocks.append(block)

        print(
            f"   ✔ Added chunk {idx} | "
            f"Page {meta.get('page')} | "
            f"Score {chunk['score']:.4f}"
        )

    print("✅ Context construction completed")
    return "\n".join(context_blocks)


def generate_answer(question: str):
    print("\n🧠 GENERATING FINAL ANSWER USING LLM")

    VECTORSTORE_DIR = "/Users/5077499/Documents/Sindhu/New/data/vectorstore"
    
    # 1️⃣ Load vector store
    collection = get_vectorstore(VECTORSTORE_DIR)
    print("✅ Vector store loaded")

    # 2️⃣ Embed query
    query_embedding = embed_query(question)
    print("✅ Query embedding created")

    # 3️⃣ Retrieve top-k chunks
    retrieved_chunks = retrieve(collection, query_embedding, k=5)

    # 4️⃣ Build context
    context = build_context(retrieved_chunks)

    # 5️⃣ Prepare prompt
    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    print("\n📤 Final prompt prepared (sending to LLM)")
    print("🤖 Sending prompt to LLM")

    # 6️⃣ Azure OpenAI Client
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION
    )

    response = client.chat.completions.create(
        model=LLM_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    print("✅ LLM response received")

    answer = response.choices[0].message.content.strip()

    print("\n" + "=" * 90)
    print("🎯 FINAL ANSWER (GROUNDED WITH CITATIONS)")
    print("=" * 90)
    print(answer)

    print("\n✅ RAG TEST COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    QUESTION = "What are flexible work arrangements and how are they approved?"
    generate_answer(QUESTION)