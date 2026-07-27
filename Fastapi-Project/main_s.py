from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class markssubmission(BaseModel):
    student_id : str
    marks : int
    subject : str


students = {
    "S001": {"name": "Ravi",    "marks": 85, "grade": "A"},
    "S002": {"name": "Priya",   "marks": 92, "grade": "A+"},
    "S003": {"name": "Amit",    "marks": 78, "grade": "B+"},
    "S004": {"name": "Sneha",   "marks": 88, "grade": "A"},
    "S005": {"name": "Rahul",   "marks": 67, "grade": "C+"},
    "S006": {"name": "Neha",    "marks": 95, "grade": "A+"},
    "S007": {"name": "Arjun",   "marks": 81, "grade": "A"},
    "S008": {"name": "Kiran",   "marks": 74, "grade": "B"},
    "S009": {"name": "Anjali",  "marks": 89, "grade": "A"},
    "S010": {"name": "Vikram",  "marks": 62, "grade": "C"}
}


@app.get("/get_students")
def get_student(id:str):
    
    if id not in students:
        raise HTTPException(
            status_code= 404,
            detail= f"student with {id} is not valid"
        )
    return {id} 


@app.post("/submit-marks")
def submit_marks(submission : markssubmission):
    if submission.student_id not in students:
        raise HTTPException(
            status_code=404,
            detail= f"student with {submission.student_id} is not valid"
        )
    
    if submission.marks < 0 or submission.marks > 100:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "marks must be between 0 and 100",
                "marks_received": submission.marks,
                "fix": "enter a valid value between 0 and 100"
            }
    )

    if submission.subject.strip == "":
         raise HTTPException(
            status_code=404,
            detail= f"student with {submission.subject} is not be empty"
        )
    
    students[submission.student_id]["marks"] = submission.marks

    return {
        "message":"marks submitted sucessfully",
        "student": students[submission.student_id]["name"],
        "subject": submission.subject,
        "marks": submission.marks
    }