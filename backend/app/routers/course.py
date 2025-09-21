from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseOut
from app.schemas.user import StudentDashboardOut   # ✅ import dashboard schema
from app.core.dependencies import require_role
from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.common import CourseOut
from app.schemas.course import CourseCreate

router = APIRouter()

# ---------------------------
# Get a single course
# ---------------------------
@router.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# ---------------------------
# Delete a course (Admin/HOD only)
# ---------------------------
@router.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin", "HOD"]))
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"msg": "Course deleted successfully"}

# ---------------------------
# Create a course (Admin/HOD only)
# ---------------------------
@router.post("/courses", response_model=CourseOut)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin", "HOD"]))
):
    new_course = Course(name=course.name, teacher_id=course.teacher_id)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# ---------------------------
# Get all courses
# ---------------------------
@router.get("/courses", response_model=list[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    try:
        courses = db.query(Course).options(joinedload(Course.teacher)).all()
        print("✅ Courses fetched:", len(courses))
        for c in courses:
            print(f"  - Course {c.id}: {c.name}")
            if c.teacher:
                print(f"    → Teacher: {c.teacher.name} (ID: {c.teacher.id})")
            else:
                print("    → Teacher: None")
        return courses
    except Exception as e:
        print("❌ Error in /courses endpoint:", str(e))
        raise  # This will still show 500, but you'll see the real error in terminal
# ---------------------------
@router.get("/student/dashboard", response_model=StudentDashboardOut)
def student_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "Student":
        raise HTTPException(status_code=403, detail="Only students can access this dashboard")

    # For now: return all courses (later filter by enrollment table)
    courses = db.query(Course).options(joinedload(Course.teacher)).all()

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "courses": courses   # ✅ return full course objects
    }

# ---------------------------
# 🚀 Seed sample courses (TEMPORARY)
# ---------------------------
@router.post("/courses/seed")
def seed_courses(db: Session = Depends(get_db)):
    sample_courses = [
        Course(name="Data Structures", teacher_id=1),
        Course(name="Web Development", teacher_id=2),
        Course(name="Machine Learning", teacher_id=3),
    ]
    db.add_all(sample_courses)
    db.commit()
    return {"msg": "Sample courses added"}