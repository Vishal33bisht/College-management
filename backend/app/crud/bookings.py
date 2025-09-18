from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from ..models import Resource, Booking
from ..schemas import BookingBase
from datetime import datetime

async def check_availability(db: AsyncSession, resource_id: int, start_time: datetime, end_time: datetime):
    result = await db.execute(select(Booking).where(
        Booking.resource_id == resource_id,
        Booking.end_time > start_time,
        Booking.start_time < end_time
    ))
    conflicts = result.scalars().all()
    return len(conflicts) == 0

async def create_booking(db: AsyncSession, booking_in: BookingBase):
    available = await check_availability(db, booking_in.resource_id, booking_in.start_time, booking_in.end_time)
    if not available:
        raise HTTPException(status_code=409, detail="Resource not available for selected time")
    booking = Booking(**booking_in.dict())
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking

async def cancel_booking(db: AsyncSession, booking_id: int):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    await db.delete(booking)
    await db.commit()
    return True

async def list_bookings(db: AsyncSession, user_id: int = None, resource_id: int = None):
    query = select(Booking)
    if user_id:
        query = query.where(Booking.user_id == user_id)
    if resource_id:
        query = query.where(Booking.resource_id == resource_id)
    result = await db.execute(query)
    return result.scalars().all()
