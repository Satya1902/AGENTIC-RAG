from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.config import get_settings
from src.database.models import DocumentChunk, QueryLog
from src.database.database_factory import DatabaseFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()
database_url = settings.database_url
db_type = settings.db_type


async def add_query_log(question: str, answer: str | None = None) -> int:
    """
    Add a new query log entry to the database.
    Args:
        question (str): User's query.
        answer (str | None): Generated answer for the query.
    Returns:
        int: ID of the newly created query log.
    Raises:
        Exception: If database insertion fails.
    """
    database = DatabaseFactory(database_url, db_type)
    AsyncSessionLocal = database.get_session()

    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                new_log = QueryLog(question=question, answer=answer)
                session.add(new_log)

            await session.commit()
            logger.info("Query log inserted successfully")

            return new_log.id

    except SQLAlchemyError as db_error:
        logger.error(f"Database error while inserting query log: {db_error}")
        raise Exception("Failed to insert query log")

    except Exception as e:
        logger.error(f"Unexpected error while inserting query log: {e}")
        raise


async def get_all_query_logs() -> list[dict]:
    """
    Retrieve all query logs ordered by latest first.
    Returns:
        list[dict]: List of query logs containing id, question, answer, and timestamp.
    Raises:
        Exception: If database retrieval fails.
    """
    database = DatabaseFactory(database_url, db_type)
    AsyncSessionLocal = database.get_session()

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(QueryLog).order_by(QueryLog.created_at.desc())
            )

            logs = result.scalars().all()

            return [
                {
                    "id": log.id,
                    "question": log.question,
                    "answer": log.answer,
                    "created_at": log.created_at.isoformat(),
                }
                for log in logs
            ]

    except SQLAlchemyError as db_error:
        logger.error(f"Database error while retrieving logs: {db_error}")
        raise Exception("Failed to retrieve query logs")

    except Exception as e:
        logger.error(f"Unexpected error while retrieving logs: {e}")
        raise


async def save_chunks_to_db(chunks: list[str],document_name: str = None) -> None:
    """
    Save document chunks into the database.
    Args:
        chunks (list[str]): List of text chunks extracted from documents.
    Returns:
        None
    Raises:
        Exception: If chunk storage fails.
    """
    database = DatabaseFactory(database_url, db_type)
    AsyncSessionLocal = database.get_session()
    await database.init_db()

    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                for idx, chunk in enumerate(chunks):
                    doc_chunk = DocumentChunk(
                        chunk_index=idx,
                        content=chunk,
                        created_at=datetime.utcnow(),
                        document_name=document_name
                    )
                    session.add(doc_chunk)

            await session.commit()

            logger.info(
                f"Chunks added successfully | count={len(chunks)} | preview={chunks[:3]}"
            )

    except SQLAlchemyError as db_error:
        logger.error(f"Database error while saving chunks: {db_error}")
        raise Exception("Failed to save document chunks")

    except Exception as e:
        logger.error(f"Unexpected error while saving chunks: {e}")
        raise


async def retrieve_top_k_chunks_from_db(query: str,top_k: int) -> list[dict]:
    """
    Retrieve the latest document chunks from the database.
    Args:
        top_k (int): Number of chunks to retrieve.
    Returns:
        list[dict]: List of document chunks with metadata.
    Raises:
        Exception: If retrieval fails.
    """
    database = DatabaseFactory(database_url, db_type)
    AsyncSessionLocal = database.get_session()

    try:
        async with AsyncSessionLocal() as session:
            tokens = [token.strip() for token in query.split() if token.strip()]
            if not tokens:
                return []
            conditions = [
                DocumentChunk.content.ilike(f"%{token}%")
                for token in tokens
            ]
            stmt = (
                select(DocumentChunk)
                .where(or_(*conditions))
                .order_by(DocumentChunk.created_at.desc())
                .limit(top_k)
            )

            result = await session.execute(stmt)
            chunks = result.scalars().all()

            return [
                {
                    "id": chunk.id,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "document_name": chunk.document_name,
                    "created_at": chunk.created_at.isoformat(),
                }
                for chunk in chunks
            ]
        
    except SQLAlchemyError as db_error:
        logger.error(f"Database error while retrieving chunks: {db_error}")
        raise Exception("Failed to retrieve document chunks")

    except Exception as e:
        logger.error(f"Unexpected error while retrieving chunks: {e}")
        raise


async def get_all_chunks_from_db() -> list[dict]:
    """
    Retrieve all chunks ordered by latest first.
    Returns:
        list[dict]: List of chunks containing id, question, answer, and timestamp.
    Raises:
        Exception: If database retrieval fails.
    """
    database = DatabaseFactory(database_url, db_type)
    AsyncSessionLocal = database.get_session()

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(DocumentChunk).order_by(DocumentChunk.created_at.desc())
            )

            chunks = result.scalars().all()

            return [
                {
                    "id": chunk.id,
                    "content": chunk.content,
                    "chunk_index": chunk.chunk_index,
                    "document_name": chunk.document_name,
                    "created_at": chunk.created_at.isoformat(),
                }
                for chunk in chunks
            ]

    except SQLAlchemyError as db_error:
        logger.error(f"Database error while retrieving chunks: {db_error}")
        raise Exception("Failed to retrieve query chunks")

    except Exception as e:
        logger.error(f"Unexpected error while retrieving chunks: {e}")
        raise