from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceOut
from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter()

# ✅ Students view their own attendance
@router.get("/attendance/me", response_model=list[AttendanceOut])
def view_my_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Student":
        raise HTTPException(status_code=403, detail="Only students can view their attendance")

    return db.query(Attendance).filter(Attendance.student_id == current_user.id).all()
