from typing import List
from pydantic import BaseModel

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from main import Agent
from chat import agent

chat_router = r = APIRouter()
summary_router = s = APIRouter()

class UsrInput(BaseModel):
    query:str

class UserInput(BaseModel):
    message: str

class ChatOutput(BaseModel):
    response: str

@s.post("")
async def summary(user_input:UsrInput):
    query = user_input.query
    agent = Agent(query)
    summary = agent.summarization()
    return {"summary": summary}

@r.post("")
async def chat(input: UserInput):
    while True:
        text_input = input.message
        if text_input == "exit":
            break
        response = agent.chat(text_input)
        return {"response" : (f"Agent: {response}")}