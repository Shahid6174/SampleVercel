from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load student data from local JSON
def load_student_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'q-vercel-python.json')  # No ".."
        
        with open(json_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("q-vercel-python.json file not found")
        return {}
    except json.JSONDecodeError:
        print("Error parsing JSON file")
        return {}

# Load once
student_data = load_student_data()

@app.get("/api")
async def get_marks(name: List[str] = Query(..., description="Student names to get marks for")):
    try:
        if not name:
            raise HTTPException(status_code=400, detail="No names provided. Use ?name=X&name=Y format")
        
        marks = []
        for student_name in name:
            marks.append(student_data.get(student_name))  # Returns None if not found
        
        return {"marks": marks}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Student Marks API",
        "usage": "/api?name=StudentName1&name=StudentName2",
        "total_students": len(student_data)
    }

# Required by Vercel to expose the FastAPI app
handler = app
