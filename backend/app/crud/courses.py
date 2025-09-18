from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from ..models import Course, Enrollment
from ..schemas import CourseCreate

async def create_course(db: AsyncSession, course_in: CourseCreate):
    course = Course(name=course_in.name, teacher_id=course_in.teacher_id)
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course

async def enroll_student(db: AsyncSession, user_id: int, course_id: int):
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment

async def list_courses(db: AsyncSession):
    result = await db.execute(select(Course))
    return result.scalars().all()
