from rank_bm25 import BM25Okapi

from src.database.chunk_service import get_all_chunks_from_db


async def retrieve_top_k_bm25_chunks(query: str, top_k: int):
    """
    Retrieve top_k chunks using BM25 lexical search.
    Args:
        query (str): User query
        top_k (int): Number of chunks to return
        all_chunks (list[dict]): Chunks fetched from DB
    Returns:
        list[dict]: Top-k relevant chunks
    """
     
    all_chunks = await get_all_chunks_from_db()
    chunks = [chunk["content"] for chunk in all_chunks]

    # Store chunks in BM25
    tokenized_corpus = [doc.split() for doc in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.split()
    
    #Retrieve top-k relevant chunks using BM25
    top_chunks = bm25.get_top_n(tokenized_query, all_chunks, n=top_k)
    return top_chunks
