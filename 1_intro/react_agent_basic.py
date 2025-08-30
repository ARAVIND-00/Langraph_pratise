from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv(dotenv_path="d:/project/langraph/.env")
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
import datetime
from langchain_openai import ChatOpenAI
import os
llm=ChatOpenAI(model="gpt-4o")

#llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")



search_tool=TavilySearch(max_results=2)

@tool
def system_time(format:str="%Y-%m-%d %H:%M:%S"):
    """
    This function return current date and time in specified format
    """

    currentime=datetime.datetime.now()
    formatted=currentime.strftime(format)
    return formatted

tools=[search_tool,system_time]
agent = create_react_agent(llm, tools)


# user_input = "when was the recent spaceX happend date? and how many days it's been since the last launch "


# for step in agent.stream({"messages": user_input},stream_mode="values",):
#     result=step["messages"][-1].pretty_print()
#     print(result)
user_input = {"messages": [{"role": "user", "content": "when was the recent spaceX happend date? and how many days it's been since the last launch "}]}

result2=agent.invoke(user_input )
for msg in result2["messages"]:
    print(msg.pretty_repr())