from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from graph import graph

app = FastAPI()

def run_graph(message : str):
  result = graph.invoke({'messages': [{"role": "user", "content": message}]})
  return result["messages"][-1].content

@app.get('/.well-known/agent-card.json')
def get_agent_card():
  return {
    "capabilities": {

    },
    "defaultInputModes": [
      "text/plain"
    ],
    "defaultOutputModes": [
      "text/plain"
    ],
    "description": "학생들의 철학 숙제나 궁금한 점을 도와줄 수 있는 agent",
    "name": "PhilosophyHelperAgent",
    "preferredTransport": "JSONRPC",
    "protocolVersion": "0.3.0",
    "skills": [
      {
        "description": "학생들이 철학 숙제를 할 때 도움을 줄 수 있는 에이전트",
        "examples": [],
        "id": "PhilosophyHelperAgent",
        "name": "model",
        "tags": [
          "llm"
        ]
      },
    ],
    "supportsAuthenticatedExtendedCard": False,
    "url": "http://localhost:8002/messages",
    "version": "0.0.1"
  }

@app.post('/messages')
async def handle_message(req: Request):
  body = await req.json()
  
  messages = body.get("params").get("message").get("parts")
  messages.reverse()
  message_text = ""
  for message in messages:
    text = message.get("text")
    message_text += f"{text}\n"

  response = run_graph(message_text)
  return {
    "message": response
  }