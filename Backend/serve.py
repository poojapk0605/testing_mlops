# serve.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from model import NEUChatbot

app = FastAPI()
chatbot = NEUChatbot()

class Query(BaseModel):
    query: str

@app.post("/query")
def query_endpoint(input_data: Query):
    response = chatbot.process_query(input_data.query)
    return {"answer": response}
