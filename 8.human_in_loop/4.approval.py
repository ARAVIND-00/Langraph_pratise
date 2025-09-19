from langgraph.graph import StateGraph,END,add_messages
from typing import TypedDict, Annotated, Sequence
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,BaseMessage
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

memory=MemorySaver()
llm=ChatOpenAI(model="gpt-4o")

search=TavilySearch()
tools=[search]

llm_with_tool=llm.bind_tools(tools)

class BasicState(TypedDict): 
    messages: Annotated[Sequence[BaseMessage], add_messages]

def model(state:BasicState):
    return{
        "messages":llm_with_tool.invoke(state["messages"])
    }

def tool_router(state:BasicState):
    last_message=state["messages"][-1]

    if(hasattr(last_message,"tool_calls")and len(last_message.tool_calls) >0):
        return "tools"
    return END

graph = StateGraph(BasicState)
graph.add_node("model", model)

graph.add_node("tools",ToolNode(tools))
graph.set_entry_point("model")

graph.add_conditional_edges("model",tool_router)
graph.add_edge("tools", "model")

app=graph.compile(checkpointer=memory, interrupt_before=["tools"])

config = {"configurable": {
    "thread_id": 1
}}

events=app.stream({
    "messages":[HumanMessage(content="What is the current weather in Chennai?")]
}    
,config=config,stream_mode="values")

for event in events:
    print("llll",event)
    print(event["messages"][-1].pretty_print())

snapshot=app.get_state(config=config).next
print("snapshot",snapshot)

choice=None
while choice not in  ["yes","no"]:
    choice=input("yes or no").strip().lower()
    if choice=="yes":
        event_countinue=app.stream(None,config=config,stream_mode="values")
        for event in event_countinue:
            print("llll2",event)
            print(event["messages"][-1].pretty_print())