from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleRequest
import requests
import os

app = FastAPI()

# ENV variables from Kubernetes
PROJECT_ID = os.environ["GCP_PROJECT"]
REGION = os.environ["GCP_REGION"]
ENDPOINT_ID = os.environ["VERTEX_ENDPOINT_ID"]
ENDPOINT_URL = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}:predict"

# Authenticate using service account key
credentials = service_account.Credentials.from_service_account_file(
    "/secrets/key.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
credentials.refresh(GoogleRequest())

class Query(BaseModel):
    query: str

@app.post("/query")
def query_vertex(input_data: Query):
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }
    payload = {
        "instances": [{"query": input_data.query}]
    }

    response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
    return response.json()
