from fastapi import FastAPI
from app.utils.test_intent import inputHandler
from app.agents.erp_agent import run_agent
import asyncio
from app.schemas.base import Input
from app.memory.mongo_memory import store_chat_history

app=FastAPI()

@app.post("/chat")
def invoke_agent(request: Input):
    #invoke agent with query and return response
    if request.file:
        text= inputHandler(request.file)
    else:
        text = request.text

    response = asyncio.run(run_agent(text))[1:]
    store_chat_history(response)
    #print("Chat history stored in db")
    return {"response": response[-1]["content"]}