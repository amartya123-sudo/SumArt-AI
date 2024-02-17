from typing import List
from pydantic import BaseModel
import regex as re

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from main import Agent
from chat import agent

chat_router = r = APIRouter()
summary_router = s = APIRouter()
suggestion_router = su = APIRouter()

class UsrInput(BaseModel):
    query:str
    length:int

class UserInput(BaseModel):
    message: str

class ChatOutput(BaseModel):
    response: str

@s.post("")
async def summary(user_input:UsrInput):
    query = user_input.query
    length = user_input.length
    summary_agent = Agent(query)
    summary = summary_agent.summarization(length)
    summary_pattern = r"<summary>\s*([^<]+)\s*<\/summary>"
    summary_match = re.search(summary_pattern, summary, re.IGNORECASE)
    keywords_pattern = r"<keywords>\s*([^<]+)\s*</keywords>"
    keywords_match = re.search(keywords_pattern, summary, re.IGNORECASE)
    if summary_match and keywords_match:
        summary = summary_match.group(1).strip()
        keywords = keywords_match.group(1).strip()
        agent = Agent(keywords)
        return [summary,agent.retrieval()]

@r.post("")
async def chat(input: UserInput):
    while True:
        text_input = input.message
        if text_input == "exit":
            break
        response = agent.chat(text_input)
        return {"response" : (f"Agent: {response}")}