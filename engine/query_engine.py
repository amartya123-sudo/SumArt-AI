from engine.tools import query_engine_tools
from llama_index import ServiceContext
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.llms import OpenAI
from llama_index.tools import QueryEngineTool, ToolMetadata

service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo"))

query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools,
    service_context=service_context    
)
tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name='sub_ques_query_engine',
            description="useful for when you want to answer queries that require analyzing"
        )
    )
]