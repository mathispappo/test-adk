from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent_loader import root_agent

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = root_agent.run(request.message)
    return {"response": response}
