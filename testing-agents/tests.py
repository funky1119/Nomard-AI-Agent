import pytest
from main import graph

@pytest.mark.parametrize(
    "email, expected_category, expected_score",
    [
        ("this is urgent!", "urgent", 10),
        ("i wanna talk to you", "normal", 5),
        ("i have an offer for you", "spam", 1),
    ]
)

# 전체 노드 테스트
def test_full_graph(email, expected_category, expected_score):
    result = graph.invoke(
        {"email": email},
        config={"configurable": {"thread_id": "1"}}
    )

    assert result["category"] == expected_category
    assert result["priority_score"] == expected_score

# 노드 개별 테스트
def test_individual_nodes():
    # categorize_email
    result = graph.nodes["categorize_email"].invoke({
        "email": "check out his offer", 
    })

    assert result["category"] == "spam"
    
    # assing_priority
    result = graph.nodes["assing_priority"].invoke({
        "category": "spam", 
    })

    assert result["priority_score"] == 1
    
    # draft_response
    result = graph.nodes["draft_response"].invoke({
        "category": "spam", 
    })

    assert "저리 가" in result["response"]


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

    assert result["priority_score"] == 1