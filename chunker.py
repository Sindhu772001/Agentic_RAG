# app/rag/chunker.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

def clean_table(table):
    """
    Cleans pdfplumber table output:
    - Converts None → ""
    - Strips whitespace
    - Removes empty rows
    """
    cleaned_rows = []

    for row in table:
        if not row:
            continue

        cleaned_row = [
            cell.strip() if isinstance(cell, str) else ""
            for cell in row
        ]

        # skip rows that are fully empty
        if any(cleaned_row):
            cleaned_rows.append(" | ".join(cleaned_row))

    return "\n".join(cleaned_rows)


def chunk_pages(pages, source):
    print("✂️ Starting chunking process")
    chunks = []

    for page in pages:
        page_no = page["page_no"]

        # TEXT CHUNKS
        text_chunks = splitter.split_text(page["text"])
        print(f"📄 Page {page_no} | Text chunks: {len(text_chunks)}")

        for text in text_chunks:
            chunk_id = str(uuid.uuid4())
            chunks.append({
                "id": chunk_id,
                "content": text,
                "metadata": {
                    "page": page_no,
                    "type": "text",
                    "source": source,
                    "chunk_id": chunk_id
                }
            })

        # TABLE CHUNKS (SAFE)
        for table in page["tables"]:
            table_text = clean_table(table)

            if not table_text.strip():
                print(f"⚠️ Empty table skipped | Page {page_no}")
                continue

            chunk_id = str(uuid.uuid4())
            chunks.append({
                "id": chunk_id,
                "content": table_text,
                "metadata": {
                    "page": page_no,
                    "type": "table",
                    "source": source,
                    "chunk_id": chunk_id
                }
            })

            print(f"📊 Table chunk created | Page {page_no}")

    print(f"✅ Total chunks created: {len(chunks)}")
    return chunks