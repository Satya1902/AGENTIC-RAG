from google.adk.agents import LlmAgent, SequentialAgent

from src.agent.query_rewriter_agent import query_rewriter_agent
from src.agent.retriever_agent import retriever_agent
from src.agent.web_agent import web_agent
from src.agent.planner_agent import planner_agent
from src.agent.evaluator_agent import evaluator_agent
from src.observability.callbacks import on_agent_end, on_agent_start

orchestrator_agent = SequentialAgent(
    name="orchestrator_agent",
    # instruction="""You are the Executive Manager responsible for the end-to-end RAG flow. 
    # YOU MUST STRICTLY EXECUTE THE FOLLOWING STEPS IN EXACT ORDER FOR EVERY QUERY. DO NOT SKIP ANY STEP.

    # STEP 1 (MANDATORY): Call the 'QueryRewriter' agent to optimize the user's request. You must wait for its response before proceeding.
    # STEP 2 (MANDATORY): Pass the rewritten query from Step 1 to the 'Planner' agent to get a logical execution roadmap.
    # STEP 3 (EXECUTION): Based strictly on the Planner's roadmap, call either the 'Retriever' agent (for internal data) OR the 'WebAssistant' agent (for live data).
    # STEP 4 (SYNTHESIS): Combine the retrieved data into a comprehensive draft answer. Do not show this draft to the user.
    # STEP 5 (MANDATORY): Pass your draft answer to the 'evaluator_agent'. 
    #     - If the Evaluator replies with 'REJECTED' or a 'Revision Request', you MUST fix the answer and evaluate it again.
    # STEP 6 (FINAL): Only after the Evaluator replies 'APPROVED', output the final response to the user.

    # CRITICAL RULE: If you attempt to answer the user without calling QueryRewriter, Planner, and evaluator_agent, you have failed your core directive.""",
    sub_agents=[query_rewriter_agent, planner_agent, retriever_agent, web_agent, evaluator_agent],
    before_agent_callback=on_agent_start,
    after_agent_callback=on_agent_end
)