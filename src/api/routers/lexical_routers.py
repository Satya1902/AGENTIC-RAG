from typing import Any
from fastapi import APIRouter, HTTPException
import logging

from src.retrieval.lexical_retriever import retrieve_top_k_bm25_chunks
from src.ingestion.pdf_loader import ingest_pdfs
from src.database.chunk_service import get_all_chunks_from_db, retrieve_top_k_chunks_from_db, save_chunks_to_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/lexical"
)


@router.post("/create_chunks")
async def load_pdfs_and_create_chunks(req_body: dict):
    """
    Creates chunks and index of multiple PDF files.
    Expects JSON: {"file_path": "src/data/sample.pdf"}
    """
    file_path = req_body.get("file_path", "src/data/satya's_resume.pdf")
    if not file_path:
        return {"error": "No file path provided"}
    
    chunks = ingest_pdfs(file_path)
    chunks_size = len(chunks)
    logger.info(f"Chunks has been created successfully for the chunk file {file_path}, with the chunks size {chunks_size} and actual chunks are {file_path}: {chunks}")
    return {"status": "success", "chunks": chunks[:100]}


@router.post("/save_chunks_to_db")
async def save_chunks_to_database(req_body: dict[str, Any]):
    """
    Retrieve all chunks from database.
    """
    # logs = await get_all_query_logs()
    chunks = req_body.get("chunks")
    document_name = req_body.get("document_name", "unknown_document.pdf")
    logger.info(f"Saving chunks to database, with the chunks size {len(chunks)} and actual chunks are {chunks}")
    try :
        await save_chunks_to_db(chunks,document_name)
        return {"status": "success", "chunks": chunks}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    


@router.post("/top_k_chunks_from_db")
async def retrieve_top_k_chunks_from_database(req_body: dict):
    """
    Retrieve all top k chunks from database.
    """
    # logs = await get_all_query_logs()
    query= req_body.get("query")
    top_k= req_body.get("top_k")
    try:
        chunks = await retrieve_top_k_chunks_from_db(query,top_k)
        return {"status": "success", "chunks": chunks}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    


@router.post("/top_k_chunks_from_db_with_bm25")
async def bm25_retrieval(req_body: dict):
    query = req_body.get("query")
    top_k = req_body.get("top_k", 5)

    try :
        top_k_chunks = await retrieve_top_k_bm25_chunks(query,top_k)
        return {"top_k_chunks": top_k_chunks}
    except Exception as e:
        logger.info(f"Error during BM25 retrieval: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during BM25 retrieval with error {str(e)}")
        
    

@router.get("/all_chunks_from_db")
async def retrieve_all_chunks_from_db():
    """
    Retrieve all chunks from database.
    """
    # logs = await get_all_query_logs()
    try:
        chunks = await get_all_chunks_from_db()
        return {"status": "success", "chunks": chunks}
    except Exception as e:
        return {"status": "error", "message": str(e)}