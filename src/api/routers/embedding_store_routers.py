from fastapi import APIRouter
import logging

from src.database.faiss_integration import add_document, get_all_documents


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/embeddings"
)


@router.post("/store_document")
async def store_embedded_document_in_database(req_body: dict):
    """
    Store a embedded document in Database.
    Expects JSON: {"title": "Agentic RAG", "content": "Welcome to Agentic RAG"}
    """
    title = req_body.get("title", "Agentic RAG")
    content = req_body.get("content", "Welcome to Agentic RAG")

    logger.info(f"Storing embeddings of content in Database: {req_body}")
    row_id = await add_document(title, content)
    return {"status": "success", "row_id": row_id, "stored_data": req_body}


@router.get("/get_documents")
async def retrieve_documents():
    """
    Retrieve all documents from database.
    """
    docs = await get_all_documents()
    return {"status": "success", "documents": docs}