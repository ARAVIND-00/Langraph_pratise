# from langchain_openai import ChatOpenAI
# from langgraph.prebuilt import create_react_agent
# from langchain_tavily import TavilySearch
# from langchain_core.tools import tool
# import datetime
# from dotenv import load_dotenv
# load_dotenv()
# from langchain import hub

# react_prompt = hub.pull("hwchase17/react")
# llm=ChatOpenAI(model="gpt-4o")

# search_tool=TavilySearch(max_results=2)
# @tool
# def system_time(format:str="%Y-%m-%d %H:%M:%S"):
#     """
#     This function return current date and time in specified format
#     """

#     currentime=datetime.datetime.now()
#     formatted=currentime.strftime(format)
#     return formatted
# tools=[system_time,search_tool]

# react_agent_runnable=create_react_agent(model=llm, tools=tools)
# agent_runnable.py
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import datetime
import os
from langchain_tavily import TavilySearch

from dotenv import load_dotenv

load_dotenv()  # Ensure OPENAI_API_KEY is loaded

# 1) Define any tools you want the agent to be able to call.
@tool
def system_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Return current system time in the given format."""
    return datetime.datetime.now().strftime(format)

search_tool=TavilySearch(max_results=2)
tools = [system_time,search_tool]

# 2) Choose your chat model
llm = ChatOpenAI(model="gpt-4o")  # or another chat-capable model

# 3) Build the prebuilt ReAct agent (messages-based interface)
# NOTE: With this prebuilt, you pass/receive ONLY `messages` when invoking.
react_agent_runnable = create_react_agent(model=llm, tools=tools)
