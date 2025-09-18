from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import Attendance
from ..schemas import AttendanceBase, AttendanceResponse
from ..deps import is_teacher, get_current_user
from sqlalchemy.future import select
from datetime import datetime

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/mark", response_model=AttendanceResponse, dependencies=[Depends(is_teacher)])
async def mark_attendance(attendance_in: AttendanceBase, db: AsyncSession = Depends(get_db)):
    attendance = Attendance(
        course_id=attendance_in.course_id,
        user_id=attendance_in.user_id,
        date=datetime.fromisoformat(attendance_in.date),
        present=attendance_in.present
    )
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    return attendance

@router.get("/", response_model=list[AttendanceResponse])
async def list_attendance(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attendance).where(Attendance.course_id == course_id))
    return result.scalars().all()
