from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import enum

class RoleEnum(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    ta = "ta"
    hod = "hod"
    admin = "admin"

class AssignmentStatusEnum(str, enum.Enum):
    submitted = "submitted"
    reviewed = "reviewed"
    graded = "graded"
    approved = "approved"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str

class CourseCreate(CourseBase):
    teacher_id: int

class CourseResponse(CourseBase):
    id: int
    teacher_id: int

    class Config:
        orm_mode = True

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        orm_mode = True

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str]
    course_id: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int
    status: AssignmentStatusEnum

    class Config:
        orm_mode = True

class SubmissionBase(BaseModel):
    assignment_id: int
    user_id: int
    file_path: str

class SubmissionResponse(SubmissionBase):
    id: int
    status: AssignmentStatusEnum

    class Config:
        orm_mode = True

class GradeBase(BaseModel):
    submission_id: int
    grader_id: int
    value: float
    approved: bool

class GradeResponse(GradeBase):
    id: int

    class Config:
        orm_mode = True

class AttendanceBase(BaseModel):
    course_id: int
    user_id: int
    date: str
    present: bool

class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        orm_mode = True

class ResourceBase(BaseModel):
    name: str
    type: str

class ResourceResponse(ResourceBase):
    id: int

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    resource_id: int
    user_id: int
    start_time: str
    end_time: str

class BookingResponse(BookingBase):
    id: int

    class Config:
        orm_mode = True
