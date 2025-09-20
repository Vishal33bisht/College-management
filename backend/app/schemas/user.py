from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List
from app.schemas.course import CourseOut  # ✅ Keep this if needed

class RoleEnum(str, Enum):
    student = "Student"
    teacher = "Teacher"
    hod = "HOD"
    admin = "Admin"
    ta = "TA"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum

    class Config:
        orm_mode = True

class StudentDashboardOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    courses: List[CourseOut]  # ✅ Still needs CourseOut

    class Config:
        orm_mode = True