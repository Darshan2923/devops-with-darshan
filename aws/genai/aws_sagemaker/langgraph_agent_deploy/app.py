from fastapi import FastAPI
from agent_graph import graph

app = FastAPI()

@app.post("/invoke")
def invoke(payload: dict):
    """
    Expected payload:
    {
      "bucket": "my-langgraph-bedrock-agent",
      "input_key": "input/input.txt",
      "output_key": "output/result.txt"
    }
    """
    return graph.invoke(payload)
