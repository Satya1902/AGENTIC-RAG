from google.adk.agents import LlmAgent

from src.observability.callbacks import on_agent_end, on_agent_start

# --- THE PLANNER ---
# This agent ONLY creates a roadmap. It does not call search tools.

planner_agent = LlmAgent(
    name="Planner",
    instruction="""You are a Strategic Query Architect. 
    - Break the user query into a logical execution plan.
    - Identify if a step depends on the output of a previous step.
    - Explicitly state whether to use 'Retriever' (for internal docs) or 'WebAssistant' (for live info).
    - Format: [Step 1: Get Project X status from Retriever], [Step 2: Check current London weather].
    - Do not answer the question; only provide the roadmap.""",
    before_agent_callback=on_agent_start,
    after_agent_callback=on_agent_end

)