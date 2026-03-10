from google.adk.agents import LlmAgent

from src.retrieval.lexical_retriever import retrieve_top_k_bm25_chunks
from src.observability.callbacks import on_agent_end, on_agent_start

# The Retriever Sub-agent
retriever_agent = LlmAgent(
    name="Retriever",
    instruction="""You are a data retrieval specialist. 
    Use BM25 for keywords/IDs, Vector for concepts/context/semantic, and Hybrid for complex queries.
    retieve the most relevant information from the internal document store based on the query if user provides top k then retrieve top k 
    else retrieve top 5 chunks.
    Always cite your specific tool source.""",
    tools=[retrieve_top_k_bm25_chunks],
    # tools=[bm25_search,vector_search,hybrid_search]
    before_agent_callback=on_agent_start,
    after_agent_callback=on_agent_end
)

