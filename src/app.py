import asyncio
import logging
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database.database_factory import DatabaseFactory
from src.api.routers.sqlite_database_routes import router as sqlite_database_router
# from src.api.routers.embedding_store_routers import router as embedding_store_router
from src.api.routers.lexical_routers import router as lexical_router
from src.config import get_settings



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()
database = DatabaseFactory(settings.database_url, settings.db_type)





@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifecycle manager.

    Runs once when the application starts and shuts down.
    """

    logger.info("Initializing database...")
    await database.init_db()
    logger.info("Database initialized successfully!")
    yield
    logger.info("Application shutdown complete.")


app = FastAPI(
    title="Agentic RAG API",
    description="API for Agentic Retrieval Augmented Generation using Gemini and Hybrid Retrieval",
    lifespan=lifespan
)



@app.post("/health",tags=["Health"])
def health_check():
    return {"health": "Health check successful!"}


@app.post("/query",tags=["Query"])
def query_agent(req_body: dict):
    logger.info(f"Received query: {req_body.get('question')}")
    return {"Answer": "Agent answer"}



app.include_router(sqlite_database_router,tags=["SQLite Database"])
app.include_router(lexical_router,tags=["Lexical"])
# app.include_router(embedding_store_router,tags=["Embedding Store"])




if __name__ == "__main__":
    settings = get_settings()
    port = settings.port

    logger.info(f"Starting server on port {port}")

    uvicorn.run(
        "src.app:app",  
        host="0.0.0.0",
        port=port,
        reload=True
    )