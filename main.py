from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from pydantic import BaseModel

from app.rag.vectorstore import get_vectorstore
from app.rag.retriever import retrieve
from app.rag.embeddings import embed_query
from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_ENDPOINT,
    LLM_DEPLOYMENT
)
from app.rag.prompt import RAG_PROMPT

from openai import AzureOpenAI

# ---------------- CONFIG ----------------
BASE_DIR = Path(__file__).resolve().parent.parent
UI_DIR = BASE_DIR / "ui"
VECTORSTORE_DIR = BASE_DIR / "data" / "vectorstore"

# ---------------------------------------

app = FastAPI(title="Agentic RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve UI folder
app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")

class ChatRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    """Serve main UI"""
    return (UI_DIR / "index.html").read_text()

@app.post("/chat")
def chat(req: ChatRequest):
    print("\n🧠 /chat request received")

    collection = get_vectorstore(str(VECTORSTORE_DIR))
    query_embedding = embed_query(req.question)
    chunks = retrieve(collection, query_embedding, k=5)

    context = "\n".join([
        f"Source: {c['metadata']['source']} | Page: {c['metadata']['page']}\n{c['content']}"
        for c in chunks
    ])

    prompt = RAG_PROMPT.format(
        context=context,
        question=req.question
    )

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

    response = client.chat.completions.create(
        model=LLM_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "Answer strictly using the context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    return {
        "answer": response.choices[0].message.content.strip()
    }


