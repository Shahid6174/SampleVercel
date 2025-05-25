from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load the student data
def load_student_data():
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to the project root
        json_path = os.path.join(current_dir, '..', 'q-vercel-python.json')
        
        with open(json_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("q-vercel-python.json file not found")
        return {}
    except json.JSONDecodeError:
        print("Error parsing JSON file")
        return {}

# Load student data once when the module loads
student_data = load_student_data()

@app.get("/api")
async def get_marks(name: List[str] = Query(..., description="Student names to get marks for")):
    """
    Get marks for specified students.
    
    Usage: /api?name=Alice&name=Bob&name=Charlie
    
    Returns marks in the same order as requested names.
    """
    try:
        if not name:
            raise HTTPException(status_code=400, detail="No names provided. Use ?name=X&name=Y format")
        
        marks = []
        
        # Look up marks for each name in the same order as requested
        for student_name in name:
            if student_name in student_data:
                marks.append(student_data[student_name])
            else:
                # Return null for students not found
                marks.append(None)  # You can change this to 0 if preferred
        
        return {"marks": marks}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Student Marks API",
        "usage": "/api?name=StudentName1&name=StudentName2",
        "total_students": len(student_data)
    }

# For Vercel, we need to expose the app
# Vercel will look for 'app' or 'handler'
handler = app