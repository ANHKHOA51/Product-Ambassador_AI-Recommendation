# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from AgenticRAG_model import find_ambassador
# from data import create_doc
# from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Extract_model import retrieve_product
from dotenv import load_dotenv

load_dotenv()
# documents = create_doc()
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# vector_store = FAISS.from_documents(documents, embeddings)
# retriever = vector_store.as_retriever(search_type="mmr", search_k=5)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    content: str


@app.get("/product/{id}")
async def product_info(id: str):
    return retrieve_product(id)

# @app.post("/analyze")
# async def func(query : Message):    
#     return find_ambassador(retriever=retriever, query=query.content)