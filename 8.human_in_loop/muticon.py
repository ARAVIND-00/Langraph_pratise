# corrected_react_linkedin.py
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.types import Command, interrupt
from typing import TypedDict, Annotated, Sequence, Dict, Any
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
import uuid
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

# --- setup ---
memory = MemorySaver()
llm = ChatOpenAI(model="gpt-4o")

class State(TypedDict):
    linkedin_topic: str
    generated_post: Annotated[Sequence[BaseMessage], add_messages]
    human_feedback: Annotated[Sequence[BaseMessage], add_messages]

# --- nodes ---
def model(state: State) -> Dict[str, Any]:
    print("[model] Generating content")
    topic = state["linkedin_topic"]

    # safe fetch: list of BaseMessage
    feedback_list = list(state.get("human_feedback", []))
    last_feedback_text = feedback_list[-1].content if feedback_list else "No feedback yet"
    print("dddd")
    prompt = f"""
LinkedIn Topic: {topic}
Human Feedback: {last_feedback_text}

Generate a structured and well-written LinkedIn post based on the given topic.
Consider previous human feedback to refine the response.
"""

    # call LLM (returns AIMessage-like object); we wrap result into AIMessage so types match
    response = llm.invoke([
        SystemMessage(content="You are an expert LinkedIn content writer"),
        HumanMessage(content=prompt)
    ])
    print("rrr",response)
    return {
        # append one AIMessage (wrapped in a list) — reducer add_messages will append it
        "generated_post": [AIMessage(content=response.content)],
        # preserve existing human_feedback (no change here)
        "human_feedback": state.get("human_feedback", [])
    }

def human_node(state: State):
    print("\n[human_node] awaiting human feedback (interrupt)...")
    generated_post = list(state.get("generated_post", []))

    payload = {
        "generated_post": generated_post,
        "message": "Provide feedback (type 'done' to finish):"
    }

    # interrupt will pause and return resume value when graph is resumed
    user_feedback = interrupt(payload)
    print(f"[human_node] Received human feedback (resume): {user_feedback}")

    fb_msg = HumanMessage(content=str(user_feedback))

    if str(user_feedback).strip().lower() == "done":
        # append final feedback then go to end
        return Command(update={"human_feedback": [fb_msg]}, goto="end_node")

    # append feedback and loop back to model
    return Command(update={"human_feedback": [fb_msg]}, goto="model")

def end_node(state: State):
    print("\n[end_node] Process finished")
    last = list(state.get("generated_post", []))[-1] if state.get("generated_post") else None
    print("Final Generated Post:", getattr(last, "content", last))
    print("Final Human Feedback:", [m.content for m in state.get("human_feedback", [])])
    return {}  # no change needed — final state is preserved

# --- graph wiring ---
graph = StateGraph(State)
graph.add_node("model", model)
graph.add_node("human_node", human_node)
graph.add_node("end_node", end_node)

graph.set_entry_point("model")
graph.add_edge(START, "model")
graph.add_edge("model", "human_node")
graph.set_finish_point("end_node")

app = graph.compile(checkpointer=memory)

# --- run ---
thread_config = {"configurable": {"thread_id": str(uuid.uuid4())}}  # string id
topic = input("Enter your LinkedIn topic: ").strip()

initial_state: State = {
    "linkedin_topic": topic,
    "generated_post": [],   # start empty lists to match schema
    "human_feedback": []
}

# stream events; stream_mode default is fine but you can use "events" or "values"
events = app.stream(initial_state, config=thread_config,)

for ev in events:
    print("dddd")
    # look for interrupt marker
    if isinstance(ev, dict) and "__interrupt__" in ev:
        # Graph paused; request user input and resume once
        print("wwwww")
        user = input("Provide feedback (or 'done' to finish): ")
        app.invoke(Command(resume=user), config=thread_config)
        # after resume, streaming will continue and produce more events
    else:
        # print debug info for event (optional)
        print("EVENT:", ev)

# After stream completes (graph finished), final state is in checkpointer
final_snapshot = app.get_state(config=thread_config).next
print("\nFinal snapshot:", final_snapshot)
