import dotenv
dotenv.load_dotenv()

import pytest
from main import graph

@pytest.mark.parametrize(
    "email, expected_category, min_score, max_score",
    [
        ("this is urgent!", "urgent", 8, 10),
        ("i wanna talk to you", "normal", 4, 7),
        ("i have an offer for you", "spam", 1, 3),
    ]
)

# 전체 노드 테스트
def test_full_graph(email, expected_category, min_score, max_score):
    result = graph.invoke(
        {"email": email},
        config={"configurable": {"thread_id": "1"}}
    )

    assert result["category"] == expected_category
    assert min_score <= result["priority_score"] <= max_score

# 노드 개별 테스트
def test_individual_nodes():
   
    # assing_priority
    result = graph.nodes["assing_priority"].invoke({
        "category": "spam", 
        "email": "buy this pot."
    })

    assert 1 <= result["priority_score"] <= 3
    
    # draft_response
    #result = graph.nodes["draft_response"].invoke({ "category": "spam" })
    #assert "저리 가" in result["response"]


def test_partial_execution():
    graph.update_state(
        config ={
            "configurable": {
                "thread_id": "1",
            }
        },
        values={
            "email": "please checkout out this offer",
            "category": "spam"
        },
        as_node="categorize_email"
    )

    result = graph.invoke(
        None, 
        config ={
            "configurable": {
                "thread_id": "1",
            }
        },
        interrupt_after="draft_response",
    )

    assert 1 <= result["priority_score"] <= 3