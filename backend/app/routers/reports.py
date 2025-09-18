from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import Attendance, Grade
from sqlalchemy.future import select

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/attendance-analytics")
async def attendance_analytics(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attendance).where(Attendance.course_id == course_id))
    records = result.scalars().all()
    total = len(records)
    present = sum(1 for r in records if r.present)
    return {"total": total, "present": present, "absent": total - present}

@router.get("/grades-analytics")
async def grades_analytics(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Grade))
    grades = [g.value for g in result.scalars().all() if g.approved]
    if not grades:
        return {"average": 0, "max": 0, "min": 0}
    return {"average": sum(grades)/len(grades), "max": max(grades), "min": min(grades)}
