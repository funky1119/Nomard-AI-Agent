from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    name="StudentHelperAgnet",
    description="An agent that can helps students with their homework",
    model=LiteLlm("openai/gpt-4o"),
    sub_agents=[]
)