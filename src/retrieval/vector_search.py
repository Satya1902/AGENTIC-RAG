from sqlalchemy import text
from database.database_factory import engine
from ingestion.embedder import get_embedding

def vector_search(query, k=5):

    embedding = get_embedding(query)

    sql = """
    SELECT content
    FROM documents
    ORDER BY embedding <-> :embedding
    LIMIT :k
    """

    with engine.connect() as conn:
        results = conn.execute(
            text(sql),
            {"embedding": embedding, "k": k}
        )

    return [r[0] for r in results]