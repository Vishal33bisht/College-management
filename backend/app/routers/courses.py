from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import courses
from ..schemas import CourseCreate, CourseResponse
from ..deps import is_teacher, is_student

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=CourseResponse, dependencies=[Depends(is_teacher)])
async def create_course(course_in: CourseCreate, db: AsyncSession = Depends(get_db)):
    return await courses.create_course(db, course_in)

@router.get("/", response_model=list[CourseResponse])
async def list_courses(db: AsyncSession = Depends(get_db)):
    return await courses.list_courses(db)

@router.post("/enroll", dependencies=[Depends(is_student)])
async def enroll(course_id: int, db: AsyncSession = Depends(get_db), user=Depends(is_student)):
    return await courses.enroll_student(db, user.id, course_id)
