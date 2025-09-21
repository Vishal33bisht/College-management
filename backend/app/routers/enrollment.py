# app/routers/enrollment.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User, RoleEnum
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.enrollment import MyCoursesOut
from app.core.dependencies import get_current_user  # adjust if needed

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/courses/{course_id}/enroll", status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can enroll")

    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    exists = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == current_user.id, Enrollment.course_id == course_id)
        .first()
    )
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already enrolled")

    enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return {"message": "Enrolled successfully"}

@router.get("/me/courses", response_model=MyCoursesOut)
def my_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Any role can call; meaningful for students
    enrollments = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.course).joinedload(Course.teacher))
        .filter(Enrollment.student_id == current_user.id)
        .all()
    )
    courses = [e.course for e in enrollments]
    return {"courses": courses}
