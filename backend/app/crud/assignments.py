from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from ..models import Assignment, Submission, AssignmentStatusEnum
from ..schemas import AssignmentCreate

async def create_assignment(db: AsyncSession, assignment_in: AssignmentCreate):
    assignment = Assignment(**assignment_in.dict())
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)
    return assignment

async def submit_assignment(db: AsyncSession, assignment_id: int, user_id: int, file_path: str):
    submission = Submission(assignment_id=assignment_id, user_id=user_id, file_path=file_path, status=AssignmentStatusEnum.submitted)
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return submission

async def review_submission(db: AsyncSession, submission_id: int):
    result = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    submission.status = AssignmentStatusEnum.reviewed
    await db.commit()
    await db.refresh(submission)
    return submission

async def grade_submission(db: AsyncSession, submission_id: int, grade_value: float):
    result = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    submission.status = AssignmentStatusEnum.graded
    # Add grade logic here
    await db.commit()
    await db.refresh(submission)
    return submission

async def approve_grade(db: AsyncSession, submission_id: int):
    result = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    submission.status = AssignmentStatusEnum.approved
    await db.commit()
    await db.refresh(submission)
    return submission
