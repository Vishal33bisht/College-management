from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os, uuid, shutil
from app.models.assignment import AssignmentUpload
from app.schemas.assignment import AssignmentOut
from app.core.dependencies import require_role
from app.database import get_db

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

# ✅ Student uploads assignment
@router.post("/assignments", response_model=AssignmentOut)
def upload_assignment(
    assignment_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(require_role(["Student"]))
):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    record = AssignmentUpload(
        student_id=user["id"],
        assignment_id=assignment_id,
        file_path=file_path
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# ✅ Teacher views submissions
@router.get("/assignments/{assignment_id}", response_model=list[AssignmentOut])
def view_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Teacher"]))
):
    return db.query(AssignmentUpload).filter(AssignmentUpload.assignment_id == assignment_id).all()
