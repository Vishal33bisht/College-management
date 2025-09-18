from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import assignments
from ..schemas import AssignmentCreate, AssignmentResponse
from ..deps import is_teacher, is_student, is_ta, is_hod
import os

router = APIRouter(prefix="/assignments", tags=["assignments"])

@router.post("/", response_model=AssignmentResponse, dependencies=[Depends(is_teacher)])
async def create_assignment(assignment_in: AssignmentCreate, db: AsyncSession = Depends(get_db)):
    return await assignments.create_assignment(db, assignment_in)

@router.post("/submit", dependencies=[Depends(is_student)])
async def submit_assignment(assignment_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db), user=Depends(is_student)):
    # Validate file size/type
    if file.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    filename = f"{user.id}_{assignment_id}_{file.filename}"
    filepath = os.path.join("uploads", filename)
    with open(filepath, "wb") as f:
        f.write(contents)
    return await assignments.submit_assignment(db, assignment_id, user.id, filepath)

@router.post("/review", dependencies=[Depends(is_ta)])
async def review_submission(submission_id: int, db: AsyncSession = Depends(get_db)):
    return await assignments.review_submission(db, submission_id)

@router.post("/grade", dependencies=[Depends(is_teacher)])
async def grade_submission(submission_id: int, grade: float, db: AsyncSession = Depends(get_db)):
    return await assignments.grade_submission(db, submission_id, grade)

@router.post("/approve", dependencies=[Depends(is_hod)])
async def approve_grade(submission_id: int, db: AsyncSession = Depends(get_db)):
    return await assignments.approve_grade(db, submission_id)
