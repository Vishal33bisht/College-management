import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
from .database import Base

class RoleEnum(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    ta = "ta"
    hod = "hod"
    admin = "admin"

class AssignmentStatusEnum(str, enum.Enum):
    submitted = "submitted"
    reviewed = "reviewed"
    graded = "graded"
    approved = "approved"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.student)
    courses = relationship("Enrollment", back_populates="user")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    user = relationship("User", back_populates="courses")
    course = relationship("Course", back_populates="enrollments")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey("courses.id"))
    status = Column(Enum(AssignmentStatusEnum), default=AssignmentStatusEnum.submitted)
    submissions = relationship("Submission", back_populates="assignment")
    course = relationship("Course", back_populates="assignments")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String)
    status = Column(Enum(AssignmentStatusEnum), default=AssignmentStatusEnum.submitted)
    assignment = relationship("Assignment", back_populates="submissions")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    grader_id = Column(Integer, ForeignKey("users.id"))
    value = Column(Float)
    approved = Column(Boolean, default=False)

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime)
    present = Column(Boolean)

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    bookings = relationship("Booking", back_populates="resource")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    resource = relationship("Resource", back_populates="bookings")
