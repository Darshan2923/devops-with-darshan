from langgraph.graph import StateGraph

# State schema (what flows through the graph)
class AgentState(dict):
    pass

def start_node(state: AgentState):
    return {"input": state["input"]}

def process_node(state: AgentState):
    text = state["input"]
    # later this will call Bedrock
    return {"output": f"Agent processed: {text}"}

# Build graph
builder = StateGraph(AgentState)

builder.add_node("start", start_node)
builder.add_node("process", process_node)

builder.set_entry_point("start")
builder.add_edge("start", "process")
builder.set_finish_point("process")

graph = builder.compile()