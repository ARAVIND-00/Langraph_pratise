from typing import TypedDict,List,Annotated
from langgraph.graph import END,StateGraph
import operator

class SimpleGraph(TypedDict):
    count:int
    sum:Annotated[int,operator.add]
    num:Annotated[List[int],operator.concat]

graph=StateGraph(SimpleGraph)


def increment(state:SimpleGraph)->SimpleGraph:
    new_count=state["count"]+1
    return {"count":new_count,
            "sum":new_count,
            "num":[new_count]}
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

state={"count":0,
       "sum":0,
       "num":[]}
result = app.invoke(state)
print(result)
