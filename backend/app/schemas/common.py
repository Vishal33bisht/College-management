from pydantic    import BaseModel, EmailStr
from typing      import Optional, List
from enum        import Enum

# --- Role enum (shared) --------------------------------
class RoleEnum(str, Enum):
    student = "Student"
    teacher = "Teacher"
    hod     = "HOD"
    admin   = "Admin"
    ta      = "TA"


# --- UserOut (for nested teacher/student info) --------
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum

    model_config = dict(from_attributes=True)  # pydantic v2


# --- CourseOut (nested teacher) -----------------------
class CourseOut(BaseModel):
    id: int
    name: str
    teacher: Optional[UserOut]  # allow null
    # (omit teacher_id if you don't need it in front end)

    model_config = dict(from_attributes=True)


# --- StudentDashboardOut (all together) --------------
class StudentDashboardOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    courses: List[CourseOut]

    model_config = dict(from_attributes=True)