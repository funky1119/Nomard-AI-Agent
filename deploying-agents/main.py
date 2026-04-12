from dotenv import load_dotenv
load_dotenv()

from agents import Agent, Runner
from fastapi import FastAPI
from openai import AsyncOpenAI
from pydantic import BaseModel

agent = Agent(
  name="Assistant", 
  instructions="너는 사용자의 질문에 답변한다.",
)

app = FastAPI()

client = AsyncOpenAI()

class CreateConversationResponse(BaseModel):
  conversation_id: str

@app.post("/conversations")
async def create_conversation() -> CreateConversationResponse:
  conversation = await client.conversations.create()
  return {
    'conversation_id': conversation.id,
  }


@app.post("/conversations/{conversation_id}/message")
async def create_message(conversation_id: str):
  pass