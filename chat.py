from engine.tools import query_engine_tools
from engine.query_engine import tools

from llama_index.agent import OpenAIAgent

tools = query_engine_tools + tools

agent = OpenAIAgent.from_tools(tools = tools)