from langgraph.types import Command
from langchain_core.tools import tool

@tool
def transfer_to_agent(agent_name: str):
    """
    지정된 에이전트로 전달합니다.

    Args:
        agent_name: 전달할 대상 에이전트 이름. 'quiz_agent', 'teacher_agent', 'feynman_agent' 중 하나여야 합니다.
    """
    return f"Transfer to {agent_name} completed."
    # return Command(
    #     goto="agent_name",
    #     graph=Command.PARENT
    # )
