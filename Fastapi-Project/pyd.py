from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class markssubmission(BaseModel):
    student_id : str
    marks : int
    subject : str



