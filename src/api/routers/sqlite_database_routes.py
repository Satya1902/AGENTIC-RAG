from fastapi import APIRouter
import logging

from src.ingestion.pdf_loader import ingest_pdfs
from src.database.chunk_service import add_query_log, get_all_query_logs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/sqlite"
)


@router.post("/store_logs")
async def store_in_sqlite(req_body: dict):
    """
    Store a string in SQLite query_logs table.
    Expects JSON: {"data": "My first query on Agentic RAG"}
    """
    question = req_body.get("question", "What is Agentic RAG?")
    answer = req_body.get("answer", "Welcome to Agentic RAG")
    if not question:
        return {"error": "No 'data' field provided"}

    logger.info(f"Storing in SQLite: {req_body}")
    row_id = await add_query_log(question, answer)
    return {"status": "success", "row_id": row_id, "stored_data": req_body}


@router.get("/logs")
async def retrieve_logs():
    """
    Retrieve all query logs from SQLite database.
    """
    logs = await get_all_query_logs()
    return {"status": "success", "logs": logs}