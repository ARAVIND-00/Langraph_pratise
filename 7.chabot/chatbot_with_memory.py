from typing import List,Annotated,TypedDict,Sequence
from langgraph.graph import END,StateGraph,add_messages
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)

memory = SqliteSaver(sqlite_conn)
# memory = MemorySaver()
llm=ChatOpenAI(model="gpt-4o")

class Basicchatstate(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]


def chatbot(state:Basicchatstate)->Basicchatstate:
    result=llm.invoke(state["messages"])
    return{"messages":result}

graph=StateGraph(Basicchatstate)

graph.add_node("chatbot",chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot",END)

app=graph.compile(checkpointer=memory)

config={"configurable":{"thread_id":1}}
while True:
    user_input=input("user:")
    if (user_input in ["exit","end"]):
        break
    else:
        result=app.invoke({
            "messages":[HumanMessage(content=user_input)]
        },config=config)
        print(result["messages"][-1].content)