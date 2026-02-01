from langgraph_agent_deploy.single_agent_graph import graph

result = graph.invoke({"input": "hello"})
print(result)