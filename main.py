from fastapi import FastAPI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pydantic import BaseModel
from Extract_model import retrieve_product
from AgenticRAG_model import find_ambassador
from dotenv import load_dotenv
from data import create_doc

load_dotenv()

documents = create_doc()
embeddings = HuggingFaceEmbeddings()
vector_store = FAISS.from_documents(documents, embeddings)

# Initialize a retriever for querying the vector store
retriever = vector_store.as_retriever(search_type="mmr", search_k=5)

app = FastAPI()

class Message(BaseModel):
    content: str

@app.post("/analyze")
async def func(query : Message):    
    return find_ambassador(retriever=retriever, query=query.content)

@app.get("/get_product/{id}")
async def product_info(id: str):
    return retrieve_product(id)