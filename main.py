import os 
from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from utils import get_recommendations, normalize_catalog  # Add normalize_catalog import
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

# ✅ Normalize the catalog after loading
CATALOG = normalize_catalog(CATALOG)

print(f"Loaded {len(CATALOG)} assessments.")

# Pydantic model
class QueryInput(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend_post(input_data: QueryInput):
    # ✅ Debugging prints
    print("Query:", input_data.query)
    descriptions = [item["description"] for item in CATALOG if "description" in item]
    print("Descriptions:", descriptions[:3])  # Show sample descriptions

    matched = get_recommendations(input_data.query, CATALOG)
    return {"recommended_assessments": matched or []}


@app.get("/recommend")
def recommend_get(query: str = Query(..., description="Query text")):
    # ✅ Debugging prints
    print("Query:", query)
    descriptions = [item["description"] for item in CATALOG if "description" in item]
    print("Descriptions:", descriptions[:3])  # Show sample descriptions

    matched = get_recommendations(query, CATALOG)
    return {"recommended_assessments": matched or []}

# Required for Render deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
