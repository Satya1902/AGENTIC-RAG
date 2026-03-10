from google.adk.agents import LlmAgent, Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# 1. Create a dedicated "Grounding" agent that ONLY handles the search tool.
# This agent acts as the bridge between the high-level WebAssistant and the raw tool.
search_agent = Agent(
    name="GoogleSearchGrounding",
    instruction="""You are a Research Specialist. 
    - Delegate search tasks with the help of google_search tool.
    - Synthesize the search results into a clean summary.
    - Always provide the source URL for information found.""",
    tools=[google_search]
)

# 2. Your WebAssistant now uses AgentTool to wrap the search_grounding_agent.
# This structure allows the Orchestrator to route to WebAssistant 
# without triggering the "Mixed Tools" error.
web_agent = Agent(
    name="WebAssistant",
    description="Root Agent",
    tools=[AgentTool(agent=search_agent)],
)

