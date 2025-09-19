from typing import TypedDict
from langgraph.graph import END,StateGraph

class SimpleGraph(TypedDict):
    count:int

graph=StateGraph(SimpleGraph)


def increment(state:SimpleGraph)->SimpleGraph:
    return {"count":state["count"]+1}
def continued(state):
    if state["count"]==5:
        return "stop"
    return "continue"


graph.add_node("increment",increment)
graph.set_entry_point("increment")
graph.add_conditional_edges("increment",continued,
                            { "stop":END,
                                "continue":"increment"
                            })
app = graph.compile()

state={"count":0}
result = app.invoke(state)
print(result)
