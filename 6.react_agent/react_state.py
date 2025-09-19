# from typing import Annotated,TypedDict,Union
# import operator

# from langchain_core.agents import AgentAction,AgentFinish

# class graphstate(TypedDict):
#     input: str
#     agent_outcome:Union[AgentAction, AgentFinish, None]
#     intermediate_steps:Annotated[list[tuple[AgentAction,str]],operator.add]

# react_state.py
from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """
    Shared state for the graph. We store the chat history in `messages`.
    The `add_messages` reducer APPENDS new messages instead of replacing the list.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
