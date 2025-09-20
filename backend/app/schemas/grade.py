from pydantic import BaseModel

class GradeCreate(BaseModel):
    student_id: int
    course_id: int
    assignment_name: str
    score: str

class GradeOut(BaseModel):
    student_id: int
    course_id: int
    assignment_name: str
    score: str

    class Config:
        orm_mode = True
