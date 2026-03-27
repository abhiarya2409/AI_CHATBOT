from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from typing import Optional

import io
from pathlib import Path
from PyPDF2 import PdfReader

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vector_store: Optional[FAISS] = None

def _extract_text_from_pdf(content_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(content_bytes))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(pages)


def process_document(content: bytes, filename: Optional[str] = None):
    global vector_store

    text = ""
    if filename and Path(filename).suffix.lower() == ".pdf":
        text = _extract_text_from_pdf(content)
    else:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1", errors="ignore")

    if not text.strip():
        raise ValueError("Uploaded document contains no text")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    vector_store = FAISS.from_texts(chunks, embeddings)


def retrieve_context(query: str) -> str:
    global vector_store

    if not vector_store:
        return ""

    docs = vector_store.similarity_search(query, k=3)
    if not docs:
        return ""

    return "\n".join([d.page_content for d in docs])