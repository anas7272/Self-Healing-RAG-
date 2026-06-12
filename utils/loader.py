from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    # BUG FIX: Old file had `docs = load_pdf(hardcoded_path)` at module level.
    # That ran on every import, crashed on any machine that wasn't the original dev's.
    # Now it's a pure function — call it explicitly where needed.
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs
