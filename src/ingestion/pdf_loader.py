import os
from pathlib import Path
import fitz  # PyMuPDF
from datetime import datetime
import logging


from src.database.database_factory import DatabaseFactory
from src.config import get_settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()
db_type = settings.db_type
database_url = settings.database_url

pdf_folder = settings.pdf_folder
chunk_word_size = settings.chunk_word_size

# ------------------------------
# PDF Loading & Chunking
# ------------------------------
def load_pdf_text(file_path: str) -> str:
    """Load full text from a PDF using PyMuPDF."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text: str, chunk_size: int) -> list[str]:
    """Split text into chunks of `chunk_size` words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

# ------------------------------
# Ingestion Function
# ------------------------------


def ingest_pdfs(source_path: str):
    """
    Ingest a single PDF file or a folder containing PDFs
    and return chunked text.
    """

    path = Path(source_path).expanduser().resolve()
    all_chunks = []

    if path.is_file() and path.suffix.lower() == ".pdf":

        full_text = load_pdf_text(path)
        chunks = chunk_text(full_text, chunk_word_size)

        logger.info(f"Ingested {path.name} with {len(chunks)} chunks.")
        all_chunks.extend(chunks)

    elif path.is_dir():

        pdf_files = list(path.rglob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {path}")
            
        for pdf_file in pdf_files:
            full_text = load_pdf_text(pdf_file)
            chunks = chunk_text(full_text, chunk_word_size)

            logger.info(f"Ingested {pdf_file.name} with {len(chunks)} chunks.")
            all_chunks.extend(chunks)

    else:
        raise ValueError(f"Invalid source path: {source_path}")

    return all_chunks