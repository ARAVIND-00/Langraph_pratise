# from langchain_core.agents import AgentFinish,AgentAction
# from langchain_core.messages import HumanMessage
# from langgraph.graph import StateGraph,END
# from node import reason_node,act_node
# from react_state import graphstate

# graph=StateGraph(graphstate)

# REASON_NODE="reason_node"
# ACT_NODE = "act_node"

# def should_continue(state:graphstate)-> str:
#     return "end" if isinstance(state['agent_outcome'],AgentFinish) else "act"
      


# graph.add_node(REASON_NODE,reason_node)
# graph.set_entry_point(REASON_NODE)
# graph.add_node(ACT_NODE,act_node)

# graph.add_conditional_edges(REASON_NODE,
#                             should_continue
#                             {
#         "act": ACT_NODE,
#         "end": END,
#     },)
# graph.add_edge(ACT_NODE, REASON_NODE)

# app = graph.compile()

# result = app.invoke(
#    {
#         "input": "How many days ago was the latest SpaceX launch?", 
#         "agent_outcome": None, 
#         "intermediate_steps": []
#     }
# )

#print(result["agent_outcome"].return_values["output"], "final result")
# graph_app.py
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from react_state import GraphState
from nodes import reason_node

# Build a very small graph: START -> reason_node -> END
graph = StateGraph(GraphState)
graph.add_node("reason", reason_node)
graph.set_entry_point("reason")
graph.add_edge("reason", END)

app = graph.compile()

if __name__ == "__main__":
    # Invoke with MESSAGES (HumanMessage). Do NOT use {"input": "..."} here.
    initial_state: GraphState = {
        "messages": [HumanMessage(content="when was the last spacex launch happend? and how many days ago was it?")]
    }

    final_state = app.invoke(initial_state)

    # Print last assistant message content (if any)
    msgs = list(final_state["messages"])
    last = msgs[-1]
    print("\n--- Final Assistant Message ---")
    print(getattr(last, "content", last))
