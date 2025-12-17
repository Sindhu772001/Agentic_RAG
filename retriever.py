# app/rag/retriever.py

from typing import List, Dict


def retrieve(collection, query_embedding: List[float], k: int = 5) -> List[Dict]:
    """
    Retrieve top-k most relevant chunks from Chroma.
    NOTE: Chroma returns distances (lower = better).
    """

    print(f"\n🔍 Retrieving top {k} chunks from vector store")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        chunk = {
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "score": results["distances"][0][i]  # distance score
        }
        retrieved_chunks.append(chunk)

    # ✅ IMPORTANT: lower distance = higher relevance
    retrieved_chunks.sort(key=lambda x: x["score"])

    print("\n🏆 Retrieved Chunks (sorted by relevance):")
    for idx, chunk in enumerate(retrieved_chunks, start=1):
        meta = chunk["metadata"]
        print(
            f"   ✔ Rank {idx} | "
            f"Page {meta.get('page')} | "
            f"Type={meta.get('type')} | "
            f"Distance={chunk['score']:.4f}"
        )

    return retrieved_chunks