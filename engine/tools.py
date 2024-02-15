from llama_index.tools import QueryEngineTool, ToolMetadata
from main import Agent

query_engine_tools = [
    QueryEngineTool(
        query_engine=Agent.query_engine,
        metadata=ToolMetadata(
            name = "summary_index",
            description="Useful to answer the questions related to the articles passed"
        )
    )
]
