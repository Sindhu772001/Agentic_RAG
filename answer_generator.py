# app/rag/answer_generator.py

from app.rag.context_builder import build_context
from app.rag.prompt import RAG_PROMPT
from app.rag.llm import generate_answer


def generate_rag_answer(question: str, retrieved_chunks: list):
    print("\n🧠 Generating RAG answer")

    if not retrieved_chunks:
        print("⚠️ No retrieved chunks")
        return "Information not found in the provided documents."

    context = build_context(retrieved_chunks)

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    print("📤 Final prompt prepared (sending to LLM)")
    answer = generate_answer(prompt)

    print("🎯 Answer generation completed")
    return answer