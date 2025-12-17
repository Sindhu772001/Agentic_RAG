# app/rag/context_builder.py

def build_context(retrieved_chunks):
    print("🧠 Building context for LLM")

    context_blocks = []

    for idx, chunk in enumerate(retrieved_chunks, start=1):
        block = f"""
[Chunk {idx}]
Score: {chunk['score']:.4f}
Source: {chunk['metadata']['source']}
Page: {chunk['metadata']['page']}
Type: {chunk['metadata']['type']}

{chunk['content']}
"""
        context_blocks.append(block)

        print(
            f"   ✔ Added chunk {idx} | "
            f"Page {chunk['metadata']['page']} | "
            f"Score {chunk['score']:.4f}"
        )

    full_context = "\n---\n".join(context_blocks)

    print("✅ Context construction completed")
    return full_context