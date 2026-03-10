from google.adk.agents import LlmAgent


from src.observability.callbacks import on_agent_end, on_agent_start

query_rewriter_agent = LlmAgent(
    name="QueryRewriter",
    instruction="""You are a Retrieval Optimizer. 
    - Rewrite the user query to maximize search hits in both Vector and BM25 systems.
    - Expand abbreviations (e.g., 'RAG' to 'Retrieval-Augmented Generation').
    - If the query is 'Who is Satya?', expand to 'Biography and professional background of Satya Nadella' if context suggests Microsoft, or keep it broad if unknown.
    - Output ONLY the rewritten query text.""",
    before_agent_callback=on_agent_start,
    after_agent_callback=on_agent_end

)