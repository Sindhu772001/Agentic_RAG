# app/rag/vectorstore.py
import chromadb

def get_vectorstore(path: str):
    print(f"📦 Initializing Chroma at: {path}")
    client = chromadb.PersistentClient(path=path)
    collection = client.get_or_create_collection("documents")
    print("✅ Chroma collection ready")
    return collection


def add_documents(collection, embedded_chunks):
    print("➕ Adding documents to vectorstore")

    collection.add(
        embeddings=[e["embedding"] for e in embedded_chunks],
        documents=[e["content"] for e in embedded_chunks],
        metadatas=[e["metadata"] for e in embedded_chunks],
        ids=[e["metadata"]["chunk_id"] for e in embedded_chunks]
    )

    print(f"✅ Documents indexed: {len(embedded_chunks)}")