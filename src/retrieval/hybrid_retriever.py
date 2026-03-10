from retrieval.vector_search import vector_search
from retrieval.lexical_retriever import bm25_search

def hybrid_search(query):

    vector_docs = vector_search(query)
    keyword_docs = bm25_search(query)

    merged = list(set(vector_docs + keyword_docs))

    return merged[:5]