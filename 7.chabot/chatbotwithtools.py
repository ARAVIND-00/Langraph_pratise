from typing import TypedDict, Annotated,Sequence
from langgraph.graph import add_messages, StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage,BaseMessage
from dotenv import load_dotenv
load_dotenv()
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

llm=ChatOpenAI(model="gpt-4o")


class Basicchatstate(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]

search_tool=TavilySearch()

tools=[search_tool]
llm_with_tool=llm.bind_tools(tools=tools)
def chatbot(state:Basicchatstate)->Basicchatstate:
    result=llm_with_tool.invoke(state["messages"])
    return{"messages":result}

def tool_router(state:Basicchatstate)->Basicchatstate:
    last_message=state["messages"][-1]
    print("lll",last_message)
    if(hasattr(last_message,"tool_calls") and len(last_message.tool_calls)>0):
        return "tool_node"
    return END

tool_node = ToolNode(tools=tools)

graph=StateGraph(Basicchatstate)
graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot",
                             tool_router,
                             )
graph.add_edge("tool_node", "chatbot")

app = graph.compile()

while True:
    user_input=input("user:")
    if (user_input in ["exit","end"]):
        break
    else:
        result=app.invoke({
            "messages":[HumanMessage(content=user_input)]
        })
        print(result)