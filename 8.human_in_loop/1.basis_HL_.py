from typing import TypedDict,Sequence,Annotated
from langchain_core.messages import HumanMessage,BaseMessage
from langgraph.graph import StateGraph,END,add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm=ChatOpenAI(model="gpt-4o")
GENERATE_POST = "generate_post"
GET_REVIEW_DECISION = "get_review_decision"
POST = "post"
COLLECT_FEEDBACK = "collect_feedback"
class State(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]


def generate_post(state:State):
    result=llm.invoke(state["messages"])
    print("--*10",type(result))
    return {
        "messages":result
    }

def get_review_decision(state:State):
    post_content=state["messages"][-1].content
    print("\n📢 Current LinkedIn Post:\n")
    print(post_content)
    print("\n")
    decision=input("Post to LinkedIn? (yes/no): ")

    if decision.lower() == "yes":
        return POST
    return COLLECT_FEEDBACK

def post(state: State):  
    final_post = state["messages"][-1].content  
    print("\n📢 Final LinkedIn Post:\n")
    print(final_post)
    print("\n✅ Post has been approved and is now live on LinkedIn!")

def collect_feedback(state: State):
    feeback=input("How can I improve this post?")
    return {
        "messages":[HumanMessage(content=feeback)]
    }

graph = StateGraph(State)

graph.add_node(GENERATE_POST, generate_post)
graph.set_entry_point(GENERATE_POST)
graph.add_node(GET_REVIEW_DECISION, get_review_decision)
graph.add_node(COLLECT_FEEDBACK, collect_feedback)
graph.add_node(POST, post)
graph.add_conditional_edges(GENERATE_POST, get_review_decision)
graph.add_edge(POST, END)
graph.add_edge(COLLECT_FEEDBACK, GENERATE_POST)

app = graph.compile()

response = app.invoke({
    "messages": [HumanMessage(content="Write me a LinkedIn post on AI Agents taking over content creation")]
})

print(response["messages"][-1].content)