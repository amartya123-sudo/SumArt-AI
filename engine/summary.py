# import json
# import os
# import faiss
# import requests
# from bs4 import BeautifulSoup
# from typing import List, Union
# import regex as re
# import app.engine.prompts as tm

# from llama_index import (
#     SummaryIndex,
#     Document,
#     StorageContext,
#     ServiceContext,
#     load_index_from_storage,
#     VectorStoreIndex,
# )
# from llama_index.vector_stores.faiss import FaissVectorStore
# from llama_index.indices.vector_store.retrievers.retriever import VectorIndexRetriever
# from llama_index.postprocessor import SentenceEmbeddingOptimizer
# from llama_index.llms.openai import OpenAI

# from app.engine.constants import STORAGE_DIR

# class Agent:
#     query_engine = None
#     def __init__(self, query:str) -> None:
#         self.query = query
#         self.method_called = False

#     def retrieval(self):
#         vector_store = FaissVectorStore.from_persist_dir(STORAGE_DIR)
#         storage_context = StorageContext.from_defaults(
#             vector_store=vector_store, persist_dir=(STORAGE_DIR)
#         )
#         index = load_index_from_storage(storage_context=storage_context)
#         retriever = VectorIndexRetriever(index=index, similarity_top_k=2)
#         nodes = retriever.retrieve(self.query)
#         response = []
#         for node in nodes:
#             response.append(node.metadata)
#         return response

#     def extract_content(self):
#         documents = []
#         for nodes in self.retrieval():
#             link = nodes['link']
#             try:
#                 response = requests.get(link)
#                 response.raise_for_status()
#                 html_content = response.text
#                 soup = BeautifulSoup(html_content, 'html.parser')
#                 paragraphs = []

#                 for p in soup.find_all('p'):
#                     paragraph_text = p.get_text().strip()
#                     if paragraph_text.startswith("At HuffPost"):
#                         break
#                     paragraphs.append(paragraph_text)
#                 content = '\n'.join(paragraphs)
#                 document = Document(
#                     text=content,
#                     metadata={
#                         'link': link
#                     }
#                 )
#                 documents.append(document)
#             except Exception as e:
#                 print(f"Error processing {link}: {e}")

#         return documents
        
#     def summarization(self):
#         llm = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0.7)
#         service_context = ServiceContext.from_defaults(llm=llm)
#         document = self.extract_content()
#         self.method_called = True
#         summary_index = SummaryIndex(
#             document,
#             service_context=service_context
#         )
#         Agent.query_engine = summary_index.as_query_engine(response_mode="tree_summarize")
#         summary = Agent.query_engine.query("Extract a concise 150 words summary of this document")
#         return summary.__dict__['response'].strip("\n")