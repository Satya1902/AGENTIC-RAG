from google.adk.agents import LlmAgent

from src.observability.callbacks import on_agent_end, on_agent_start

# CHANGE: Removed orchestrator from sub_agents to avoid circular dependency
evaluator_agent = LlmAgent(
    name="evaluator_agent",
    instruction="""You are the Final Quality Gate.
    - Review the synthesized answer provided by the Orchestrator.
    - **Check**: Accuracy against retrieved snippets, completeness, and formatting.
    - **Rejection**: If the answer is missing key info or contains hallucinations, output 'REJECTED' followed by a 'Revision Request' explaining what to fix.
    - **Approval**: If perfect, output 'APPROVED' and summarize why.
    - Your feedback is for the Orchestrator's internal use.""",
    before_agent_callback=on_agent_start,
    after_agent_callback=on_agent_end
)