from typing import Literal, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

class EmailState(TypedDict):
    email: str
    category: Literal["spam", "normal", "urgent"]
    priority_score: int
    response: str

def categorize_email(state: EmailState):
    email = state['email'].lower()

    if "urgent" in email or "asap" in email:
        category = "urgent"
    elif "offer" in email or "discount" in email:
        category = "spam"
    else:
        category = "normal"

    return {"category": category}



def assing_priority(state: EmailState):
    scores = {
        "urgent": 10,
        "normal": 5,
        "spam": 1
    }
    return {"priority_score": scores[state["category"]]}

def draft_response(state: EmailState):
    responses = {
        "urgent": "가능한 빨리 대답해 줄게",
        "normal": "곧 다시 연락할게",
        "spam":  "저리 가"
    }
    return {"response": responses[state['category']]}

graph_builder = StateGraph(EmailState)

graph_builder.add_node("categorize_email", categorize_email)
graph_builder.add_node("assing_priority", assing_priority)
graph_builder.add_node("draft_response", draft_response)

graph_builder.add_edge(START, "categorize_email")
graph_builder.add_edge("categorize_email", "assing_priority")
graph_builder.add_edge("assing_priority", "draft_response")
graph_builder.add_edge("draft_response", END)

graph = graph_builder.compile(checkpointer=checkpointer)
