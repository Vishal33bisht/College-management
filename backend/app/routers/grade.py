from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeOut
from app.core.dependencies import require_role
from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter()

# ---------------------------
# Teachers input grades
# ---------------------------
@router.post("/grades", response_model=GradeOut)
def input_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Teacher"]))
):
    new_grade = Grade(**grade.dict())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

# ---------------------------
# Students view their grades
# ---------------------------
@router.get("/grades/me", response_model=list[GradeOut])
def view_my_grades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Student":
        raise HTTPException(status_code=403, detail="Only students can view their grades")

    return db.query(Grade).filter(Grade.student_id == current_user.id).all()
