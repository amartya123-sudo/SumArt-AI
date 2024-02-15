import json
import os
import faiss
from llama_index import (
    Document,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.vector_stores.faiss import FaissVectorStore

with open('data.json', 'r') as f:
    data = json.load(f)

documents = []
for item in data:
    document = Document(
        text=item['short_description'],
        metadata={
            'id':item['id'],
            'category': item['category'],
            'link': item['link'],
            'headline':item['headline']

        }
    )
    documents.append(document)

d = 1536
faiss_index = faiss.IndexFlatL2(d)
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True
)

index.storage_context.persist()