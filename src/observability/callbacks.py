import time
from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.genai import types



def on_agent_start(callback_context: CallbackContext) -> Optional[types.Content]:
    print("inside before_agent_callback")

    agent_name = callback_context.agent_name
    print(f"\n🔵 [Observability] Entering: {agent_name}")

    # Access current state
    current_flow = callback_context.state.get("agent_flow", [])
    start_times = callback_context.state.get("agent_start_times", {})

    # Update state directly
    current_flow.append(agent_name)
    start_times[agent_name] = time.time()

    callback_context.state["agent_flow"] = current_flow
    callback_context.state["agent_start_times"] = start_times

    return None

def on_agent_end(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    
    # 1. Calculate Latency
    start_times = callback_context.state.get("agent_start_times", {})
    latencies = callback_context.state.get("agent_latencies", {})
    
    if agent_name in start_times:
        duration = round(time.time() - start_times[agent_name], 3)
        latencies[agent_name] = duration
        callback_context.state["agent_latencies"] = latencies
        print(f"✅ [Observability] {agent_name} completed in {duration}s")

    # 2. Capture Output
    agent_outputs = callback_context.state.get("agent_outputs", {})
    
    # Extract text safely
    output_text = ""
    # Use callback_context instead of ctx
    if hasattr(callback_context, 'output') and callback_context.output and callback_context.output.parts:
        output_text = "\n".join([p.text for p in callback_context.output.parts if hasattr(p, 'text') and p.text])
    
    agent_outputs[agent_name] = output_text
    callback_context.state["agent_outputs"] = agent_outputs

    return None