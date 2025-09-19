from typing import List,Annotated,TypedDict,Sequence
from langgraph.graph import END,StateGraph,add_messages
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

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

app=graph.compile()

while True:
    user_input=input("user:")
    if (user_input in ["exit","end"]):
        break
    else:
        result=app.invoke({
            "messages":[HumanMessage(content=user_input)]
        })
        print(result)