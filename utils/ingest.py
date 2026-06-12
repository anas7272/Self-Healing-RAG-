import sys
import os

# Add project root to path so imports work when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_chroma import Chroma
from utils.loader import load_pdf
from utils.chunker import split_documents
from utils.embeddings import get_embeddings


def ingest(pdf_path: str):
    # BUG FIX: Old file had hardcoded Windows path and ran at module level.
    # Now accepts pdf_path as argument — works on any machine.
    print(f"Loading PDF: {pdf_path}")
    docs = load_pdf(pdf_path)

    print(f"Splitting into chunks...")
    chunks = split_documents(docs)

    print(f"Embedding and storing {len(chunks)} chunks...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory="vectorstore"
    )

    print(f"✅ Done. {len(chunks)} chunks stored in vectorstore/")
    return vectordb


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <path_to_pdf>")
        print("Example: python ingest.py Company_FAQ.pdf")
        sys.exit(1)

    ingest(sys.argv[1])
