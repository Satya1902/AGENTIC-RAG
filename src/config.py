import os
from dotenv import dotenv_values
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"
    allow_methods: str = "GET,POST,OPTIONS,DELETE,PUT"
    allow_headers: str = "Authorization,Content-Type,Accept,Origin,User-Agent,X-Requested-With,X-API-Key,X-Session-Id,X-Usecase-Id,X-Correlation-ID,x-base-api-key,token"

    app_name: str = "agentic_rag_app"
    user_id: str = "satya1902"

    #database
    db_type: str = "sqlite"
    database_url: str = "sqlite+aiosqlite:///./agentic_rag.db"
    supported_db_engines: list[str] = ["sqlite", "postgresql", "postgresql+pgvector"]


    #ingestion
    pdf_folder : str = "src/data"
    chunk_word_size : int = 300
    embedding_dim : int = 384
    top_k : int = 5

    #llm
    # GEMINI_API_KEY="AIzaSyACkOsQ5qyfHFm5HYhkZOKCpM44hTOw2Mg"
    # GEMINI_API_KEY="AIzaSyCBPdkDqC7noS2KLkzgAhxkI7Rra5QP46E"
    # GEMINI_API_KEY="AIzaSyBTShhBCiXfBbZ0ZrtETuspC7X0FYEq8ZI"
    # GEMINI_API_KEY=AIzaSyDeVJIAqvBthFQKqquECPfKozOtclHWNn0
    gemini_api_key : str ="AIzaSyBKn6GdM_DeotYVsHndXYT6v30W1yVVEPA"
    google_api_key : str ="AIzaSyBKn6GdM_DeotYVsHndXYT6v30W1yVVEPA"
    gemini_model : str = "gemini-2.5-flash"
    transformer_model : str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model : str = "all-MiniLM-L6-v2"
    
    #faiss
    faiss_index_path: str = "faiss.index"
  
    # memory
    mem0_api_key : str = "m0-PBEtcehQxEsKJS5CXgxNhSxPQ247iy6gWR9rwoc0"

    #pdf
    pdf : str = "fitz" 

    base_url : str = "http://localhost"
    port : int = 4000






def get_settings() -> Settings:
    return Settings()
