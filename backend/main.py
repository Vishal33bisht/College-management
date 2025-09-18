from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import shutil, os, uuid

app = FastAPI(title="College Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Security ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
USERS = {
    "student@example.com": {"password": "password", "role": "student", "name": "Student One"},
    "teacher@example.com": {"password": "password", "role": "teacher", "name": "Teacher One"},
    "hod@example.com": {"password": "password", "role": "hod", "name": "HOD One"},
}

# --- Models ---
class RegisterUser(BaseModel):
    name: str
    email: str
    password: str
    role: str  # student | teacher | hod

class LoginUser(BaseModel):
    email: str
    password: str
    role: str

# ------------------- ROUTES -------------------

@app.get("/")
def home():
    return {"message": "Welcome to College Management API 🚀"}

# --- Register ---
@app.post("/register")
def register(user: RegisterUser):
    if user.email in USERS:
        raise HTTPException(status_code=400, detail="User already exists")
    USERS[user.email] = {
        "password": user.password,
        "role": user.role,
        "name": user.name,
    }
    return {
        "msg": "User registered successfully ✅",
        "user": {"name": user.name, "email": user.email, "role": user.role},
    }

# --- Login ---
@app.post("/login")
def login(user: LoginUser):
    u = USERS.get(user.email)
    if not u or u["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if u["role"] != user.role:
        raise HTTPException(status_code=401, detail="Role mismatch")
    token = f"demo-token:{user.email}:{u['role']}"
    return {"access_token": token, "token_type": "bearer", "role": u["role"], "name": u["name"]}

@app.post("/token")
def login_token(username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    u = USERS.get(username)
    if not u or u["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if u["role"] != role:
        raise HTTPException(status_code=401, detail="Role mismatch")
    token = f"demo-token:{username}:{u['role']}"
    return {"access_token": token, "token_type": "bearer"}

# --- Current user ---
def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token or not token.startswith("demo-token:"):
        raise HTTPException(status_code=401, detail="Invalid token")
    parts = token.split("demo-token:")[1].split(":")
    if len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid token format")
    username, role = parts
    user = USERS.get(username)
    if not user or user.get("role") != role:
        raise HTTPException(status_code=401, detail="Invalid token user/role")
    return {"email": username, "role": user["role"], "name": user["name"]}

@app.get("/me")
def me(current=Depends(get_current_user)):
    return current


@app.get("/courses")
def get_courses(current=Depends(get_current_user)):
    return [
        {"id": 1, "name": "Mathematics", "teacher": "Dr. Sharma"},
        {"id": 2, "name": "Physics", "teacher": "Prof. Verma"},
        {"id": 3, "name": "Computer Science", "teacher": "Ms. Gupta"},
    ]

@app.get("/attendance")
def get_attendance(current=Depends(get_current_user)):
    return [
        {"course": "Mathematics", "attendance": "85%"},
        {"course": "Physics", "attendance": "92%"},
        {"course": "Computer Science", "attendance": "78%"},
    ]

@app.get("/grades")
def get_grades(current=Depends(get_current_user)):
    return [
        {"course": "Mathematics", "assignment": "A", "exam": "B+"},
        {"course": "Physics", "assignment": "B", "exam": "A"},
        {"course": "Computer Science", "assignment": "A+", "exam": "A"},
    ]

# --- Assignment Upload ---
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/submit-assignment")
def submit_assignment(
    assignment_id: int = Form(...),
    file: UploadFile = File(...),
    current=Depends(get_current_user),
):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    dest = os.path.join(UPLOAD_DIR, filename)
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "msg": "Assignment uploaded successfully ✅",
        "file_path": dest,
        "assignment_id": assignment_id,
        "uploaded_by": current["email"],
    }

# --- Resource Booking ---
@app.post("/book")
def book_resource(
    resource: str = Form(...),
    timeslot: str = Form(...),
    current=Depends(get_current_user),
):
    booking_id = uuid.uuid4().hex[:8]
    return {
        "msg": "Booking successful ✅",
        "booking_id": booking_id,
        "resource": resource,
        "timeslot": timeslot,
        "requested_by": current["email"],
    }
