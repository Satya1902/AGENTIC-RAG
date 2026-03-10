import os
import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config import get_settings
from src.database.models import Document
from database.database_factory import DatabaseFactory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

settings = get_settings()
FAISS_INDEX_PATH = settings.faiss_index_path
EMBEDDING_MODEL = SentenceTransformer(settings.embedding_model)
EMBEDDING_DIM = settings.embedding_dim
database_url = settings.database_url
db_type = settings.db_type


# Initialize the database factory
db_factory = DatabaseFactory(database_url, db_type)  # This will use settings.database_url


def load_faiss_index(dim: int = 384):
    """Load or create FAISS index"""
    if os.path.exists(FAISS_INDEX_PATH):
        index = faiss.read_index(FAISS_INDEX_PATH)
        logger.info(f"Loaded FAISS index from {FAISS_INDEX_PATH}")
    else:
        index = faiss.IndexFlatL2(dim)
        faiss.write_index(index, FAISS_INDEX_PATH)
        logger.info(f"Created new FAISS index at {FAISS_INDEX_PATH}")
    return index


async def add_document(title: str, content: str):
    """Add document embedding to FAISS and store in DB via SQLAlchemy"""
    index = load_faiss_index(EMBEDDING_DIM)
    embedding = EMBEDDING_MODEL.encode([content]).astype("float32")
    vector_id = index.ntotal  # ID in FAISS
    index.add(embedding)
    faiss.write_index(index, FAISS_INDEX_PATH)
    logger.info(f"Added document embedding to FAISS index, vector_id={vector_id}")

    # Store document in database
    try:
        async with db_factory.get_session()() as session:  # Use factory session
            async with session.begin():
                doc = Document(title=title, content=content, vector_id=vector_id)
                session.add(doc)
            await session.commit()
            await session.refresh(doc)
            logger.info(f"Document stored in database with id={doc.id}")
            return doc.id
    except Exception as e:
        logger.exception(f"Failed to store document in database: {e}")
        raise


async def get_all_documents():
    """Retrieve all documents from database"""
    try:
        async with db_factory.get_session()() as session:
            result = await session.execute(select(Document))
            documents = result.scalars().all()
            logger.info(f"Retrieved {len(documents)} documents from DB")
            return documents
    except Exception as e:
        logger.exception(f"Failed to retrieve documents: {e}")
        raise