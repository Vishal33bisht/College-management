from __future__ import annotations
from pydantic import BaseModel

class CourseCreate(BaseModel):
    name: str
    teacher_id: int

class CourseOut(BaseModel):
    id: int
    name: str
    teacher_id: int
    teacher: 'UserOut'  # 👈 forward reference (no import needed!)

    class Config:
        orm_mode = True