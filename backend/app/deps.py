from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .auth import decode_access_token
from .models import User, RoleEnum
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def is_student(user: User = Depends(get_current_user)):
    if user.role != RoleEnum.student:
        raise HTTPException(status_code=403, detail="Not a student")
    return user

def is_teacher(user: User = Depends(get_current_user)):
    if user.role != RoleEnum.teacher:
        raise HTTPException(status_code=403, detail="Not a teacher")
    return user

def is_ta(user: User = Depends(get_current_user)):
    if user.role != RoleEnum.ta:
        raise HTTPException(status_code=403, detail="Not a TA")
    return user

def is_hod(user: User = Depends(get_current_user)):
    if user.role != RoleEnum.hod:
        raise HTTPException(status_code=403, detail="Not a HOD")
    return user

def is_admin(user: User = Depends(get_current_user)):
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not an admin")
    return user
