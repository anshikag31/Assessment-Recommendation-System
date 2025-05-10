import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from utils import get_recommendations
from fastapi import Query

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load catalog from assessments.json
assessments_path = os.path.join(os.path.dirname(__file__), "assessments.json")

if os.path.exists(assessments_path) and os.path.getsize(assessments_path) > 0:
    with open(assessments_path, "r", encoding="utf-8") as f:
        CATALOG = json.load(f).get("recommended_assessments", [])
else:
    CATALOG = []

print(f"Loaded {len(CATALOG)} assessments.")

# Pydantic model
class QueryInput(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recommend")
def recommend_get(query: str = Query(..., description="Query text")):
    matched = get_recommendations(query, CATALOG)
    if not matched:
        return {"recommended_assessments": []}
    return {"recommended_assessments": matched}

# Required for Render deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
