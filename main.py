from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import os
from typing import List
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from utils import get_recommendations  # Ensure this is the correct path to your utility function

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from any origin (you can restrict this if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with a list of specific origins for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods like GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
)

# Load catalog (ensure the file exists and has the expected content)
assessments_path = os.path.join(os.path.dirname(__file__), "assessments.json")



#assessments_path = r"C:\Users\KIIT\Documents\shl_cv_parser\assessments.json"

if os.path.exists(assessments_path) and os.path.getsize(assessments_path) > 0:
    with open(assessments_path, "r", encoding="utf-8") as f:
        CATALOG = json.load(f).get("recommended_assessments", [])
else:
    CATALOG = []

print(f"Loaded {len(CATALOG)} assessments.")

# Pydantic model for query input
class QueryInput(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(data: QueryInput):
    query = data.query
    
    # Get recommendations based on the query
    matched = get_recommendations(query, CATALOG)
    
    if not matched:
        return {"recommended_assessments": []}  # If no match found, return empty list
    
    return {"recommended_assessments": matched}  # Return matched assessments
