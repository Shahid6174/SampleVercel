from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load JSON data
def load_student_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'q-vercel-python.json')

        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load JSON: {e}")
        return {}

student_data = load_student_data()

@app.get("/api")
async def get_marks(name: List[str] = Query(...)):
    if not name:
        raise HTTPException(status_code=400, detail="No names provided")
    
    marks = [student_data.get(n) for n in name]
    return {"marks": marks}

@app.get("/")
async def root():
    return {
        "message": "Student Marks API running on Vercel",
        "usage": "/api?name=Alice&name=Bob"
    }

handler = app  # Required for Vercel
