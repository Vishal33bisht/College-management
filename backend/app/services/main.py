from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routers import auth, course, attendance, grade, assignment, enrollment

# Database + Models
from app.database import Base, engine
from app.models import user, course as course_model, attendance as attendance_model, grade as grade_model, assignment as assignment_model

# ✅ Create app instance first
app = FastAPI(title="College Management System API")

# ✅ CORS setup
origins = [
    "http://localhost:5173",   # React dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create tables automatically (dev mode)
Base.metadata.create_all(bind=engine)

# ✅ Include routers (after app is created)
app.include_router(auth.router)
app.include_router(course.router)
app.include_router(attendance.router)
app.include_router(grade.router)
app.include_router(assignment.router)
app.include_router(enrollment.router)  # ✅ moved here, after app creation
