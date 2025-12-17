import os

from app.rag.loader import load_pdf
from app.rag.chunker import chunk_pages
from app.rag.embeddings import embed_chunks
from app.rag.vectorstore import get_vectorstore, add_documents

DATA_DIR = "data/docs"
VECTORSTORE_DIR = "data/vectorstore"


def run_indexing():
    print("\n🚀 STARTING DOCUMENT INDEXING PIPELINE\n")

    collection = get_vectorstore(VECTORSTORE_DIR)

    pdf_files = [
        f for f in os.listdir(DATA_DIR)
        if f.lower().endswith(".pdf")
    ]

    print(f"📂 PDFs found for indexing: {len(pdf_files)}")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(DATA_DIR, pdf_file)
        print(f"\n📘 Processing file: {pdf_file}")

        # 1️⃣ Load PDF
        pages = load_pdf(pdf_path)

        # 2️⃣ Chunk
        chunks = chunk_pages(pages, source=pdf_file)

        if not chunks:
            print(f"⚠️ No chunks created for {pdf_file}, skipping")
            continue

        # 3️⃣ Embed
        embedded_chunks = embed_chunks(chunks)

        # 4️⃣ Store
        add_documents(collection, embedded_chunks)

        print(f"✅ Completed indexing for: {pdf_file}")

    print("\n🎉 INDEXING COMPLETED SUCCESSFULLY\n")


if __name__ == "__main__":
    run_indexing()