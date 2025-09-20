from pydantic import BaseModel
from datetime import date

class AttendanceCreate(BaseModel):
    course_id: int
    student_id: int
    date: date
    status: str  # "Present" or "Absent"

class AttendanceOut(BaseModel):
    course_id: int
    student_id: int
    date: date
    status: str

    class Config:
        orm_mode = True
