from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import bookings
from ..schemas import BookingBase, BookingResponse
from ..deps import get_current_user
from datetime import datetime

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse)
async def create_booking(booking_in: BookingBase, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    booking_in.user_id = user.id
    booking_in.start_time = datetime.fromisoformat(booking_in.start_time)
    booking_in.end_time = datetime.fromisoformat(booking_in.end_time)
    return await bookings.create_booking(db, booking_in)

@router.delete("/{booking_id}")
async def cancel_booking(booking_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await bookings.cancel_booking(db, booking_id)

@router.get("/", response_model=list[BookingResponse])
async def list_bookings(user_id: int = None, resource_id: int = None, db: AsyncSession = Depends(get_db)):
    return await bookings.list_bookings(db, user_id, resource_id)
