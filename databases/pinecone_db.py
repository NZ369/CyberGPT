import os
import pinecone
from dotenv import load_dotenv
from langchain.vectorstores import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
index_name = 'test-index'

def pinecone_init():
    pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENVIRONMENT,
    )

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, metric='cosine', dimension=1536)

def pinecone_from_documents(docs, embeddings, index_name):
    pinecone_init()
    return Pinecone.from_documents(documents=docs, embedding=embeddings, index_name=index_name).as_retriever()