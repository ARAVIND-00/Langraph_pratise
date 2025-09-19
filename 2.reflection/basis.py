from typing import List, Sequence,TypedDict,Annotated
from langgraph.graph import END,StateGraph
from langchain_core.messages import BaseMessage,HumanMessage
from chain import generation_chain, reflection_chain
from langgraph.graph.message import add_messages





REFLECT = "reflect"
GENERATE = "generate"

class GraphState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

graph = StateGraph(GraphState)

def generate_node(state: GraphState):

    result =generation_chain.invoke({"messages":state["messages"]})
    return {"messages": state["messages"] + [result]}
    

def reflect_node(state: GraphState):
    response = reflection_chain.invoke({"messages": state["messages"]})
    return {"messages": state["messages"] + [HumanMessage(content=response.content)]}

def should_continue(state: GraphState):
    if len(state["messages"])>6:
        return "end"
    return "reflect"

graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)
graph.add_conditional_edges(
    GENERATE,
      should_continue,
      {
        "reflect": REFLECT,  # label -> node key
        "end": END,          # label -> END sentinel
    },
                            )
graph.add_edge(REFLECT, GENERATE)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()
app.get_graph().draw_mermaid_png()

response=app.invoke({
    "messages": [HumanMessage(content="AI Agents taking over content creation")]
    })

print(response)
