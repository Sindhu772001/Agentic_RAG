# app/rag/loader.py
import pdfplumber

def load_pdf(pdf_path: str):
    print(f"📄 Loading PDF: {pdf_path}")
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        print(f"📘 Pages found: {len(pdf.pages)}")

        for idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            tables = page.extract_tables() or []

            print(
                f"➡️ Page {idx} | "
                f"text_length={len(text)} | "
                f"tables={len(tables)}"
            )

            pages.append({
                "page_no": idx,
                "text": text,
                "tables": tables
            })

    print("✅ PDF loading completed")
    return pages