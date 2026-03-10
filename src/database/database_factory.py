import logging
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from src.config import get_settings
from src.database.models import Base
from src.database import models 

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
settings = get_settings()
SUPPORTED_DB_ENGINES = settings.supported_db_engines 

class DatabaseFactory:
    """
    Factory for creating async database sessions for multiple database types.
    Supports SQLite, PostgreSQL (with pgvector), and can be extended to other databases.
    """

    def __init__(self, database_url: str = "sqlite+aiosqlite:///./agentic_rag.db", db_type: str = "sqlite"):
        """
        Initialize the factory with a database type.
        :param db_type: Type of database, e.g., "sqlite", "postgresql"
        """
        self.database_url = database_url
        self.db_type = db_type.lower()
        if self.db_type not in SUPPORTED_DB_ENGINES:
            raise ValueError(f"Unsupported database type: {self.db_type}")
        self.engine = None
        self.AsyncSessionLocal = None
        self._create_engine()

    def _create_engine(self):
        """Create async engine and sessionmaker"""
        if self.db_type == "sqlite":
            try:
                logger.info(f"Creating database engine for type '{self.db_type}' with URL: {self.database_url}")
                self.engine = create_async_engine(self.database_url, echo=True)
                self.AsyncSessionLocal = sessionmaker(
                    bind=self.engine,
                    expire_on_commit=False,
                    class_=AsyncSession
                )
                logger.info("Database engine created successfully!")
            except (SQLAlchemyError, DBAPIError) as e:
                logger.exception(f"Failed to create database engine: {e}")
                raise

    async def init_db(self):
        """Create all tables in the database"""
        if self.db_type == "sqlite":
            try:
                async with self.engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                logger.info("Database tables initialized successfully!")
            except (SQLAlchemyError, DBAPIError) as e:
                logger.exception(f"Error initializing database tables: {e}")
                raise

    def get_session(self) :
        """Get a new async session"""
        if self.db_type == "sqlite":
            try:
                return self.AsyncSessionLocal
            except (SQLAlchemyError, DBAPIError) as e:
                logger.exception(f"Error creating database session: {e}")
                raise