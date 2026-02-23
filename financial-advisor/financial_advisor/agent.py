from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("openai/gpt-4o")


def get_game(game: str):
    return f"{game}의 동시 접속자 수는 30만명 입니다."


def total_price(price: int):
    return f"게임의 가격은 {price}원 입니다."


lol_agent = Agent(
    name="LolAgent",
    instruction="너는 리그오브레전드에 관한 질문을 도와줄거야",
    model=MODEL,
    description="리그오브레전드 관련된 질문이 있으면 이 agent로 전송하는 거야",
)

game_agent = Agent(
    name="gameAgent",
    instruction="너는 게임 관련 질문을 받아서 사용자를 도와줄 거야",
    model=MODEL,
    tools=[
        get_game,
        total_price,
    ],
    sub_agents=[lol_agent],
)

root_agent = game_agent
