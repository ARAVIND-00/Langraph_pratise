# from agent_runnable import tools,react_agent_runnable
# from react_state import graphstate

# def reason_node(state:graphstate):
#     agent_outcome=react_agent_runnable.invoke(state)
#     return {
#         "agent_outcome":agent_outcome
#     }

# def act_node(state:graphstate):
#     agent_action=state["agent_outcome"]
#     tool_name=agent_action.tool
#     tool_input=agent_action.tool_input
#     tool_function=None

#     for tool in tools:
#         if tool.name==tool_name:
#             tool_function=tool
#             break
#     if tool_function:
#         if isinstance(tool_input, dict):
#             output = tool_function.invoke(**tool_input)
#         else:
#             output = tool_function.invoke(tool_input)
#     else:
#         output = f"Tool '{tool_name}' not found"
    
#     return {"intermediate_steps": [(agent_action, str(output))]}

# nodes.py
from typing import Dict, Any
from langchain_core.messages import BaseMessage
from agent_runnable import react_agent_runnable
from react_state import GraphState

def reason_node(state: GraphState) -> Dict[str, Any]:
    """
    Single-step node that hands off the current message history to the
    prebuilt ReAct agent and returns the updated messages.

    IMPORTANT:
    - We only return {"messages": ...} so the reducer appends/merges correctly.
    - We DO NOT construct or pass classic ReAct variables (input/tools/...).
    """
    # Call the prebuilt agent WITH messages
    result = react_agent_runnable.invoke({"messages": state["messages"]})
    # Prebuilt returns {"messages": [...]} — propagate them forward.
    return {"messages": result["messages"]}
