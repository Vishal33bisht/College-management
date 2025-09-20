from pydantic import BaseModel

class AssignmentOut(BaseModel):
    id: int
    student_id: int
    assignment_id: int
    file_path: str

    class Config:
        orm_mode = True
