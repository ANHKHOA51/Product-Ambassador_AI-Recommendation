from fastapi import FastAPI
from pydantic import BaseModel
from models import get_agent, retrieve_product

app = FastAPI()

class Message(BaseModel):
    content: str

@app.post("/analyze")
async def func(query : Message):    
    agent = get_agent()
    response = agent.run(query.content + " chỉ cần cho biết tên 3 người phù hợp nhất")

    return {"response": response}

@app.get("/get_product/{id}")
async def product_info(id: str):
    return retrieve_product(id)


