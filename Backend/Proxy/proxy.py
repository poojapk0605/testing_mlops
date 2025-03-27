# proxy.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
import requests
import os

app = FastAPI()

# Set these as ENV variables in your deployment
PROJECT_ID = os.environ["GCP_PROJECT"]
REGION = os.environ["GCP_REGION"]
ENDPOINT_ID = os.environ["VERTEX_ENDPOINT_ID"]
ENDPOINT_URL = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}:predict"

class Query(BaseModel):
    query: str

@app.post("/query")
def query_vertex(input_data: Query):
    token = id_token.fetch_id_token(GoogleRequest(), ENDPOINT_URL)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"instances": [{"query": input_data.query}]}
    res = requests.post(ENDPOINT_URL, headers=headers, json=payload)
    return res.json()
