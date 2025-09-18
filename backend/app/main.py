from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, courses, assignments, attendance, bookings, reports
import os

app = FastAPI()

# CORS config: restrict origins for production
origins = [
    os.getenv("CORS_ORIGIN", "http://localhost:5173")
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Routers
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(assignments.router)
app.include_router(attendance.router)
app.include_router(bookings.router)
app.include_router(reports.router)
