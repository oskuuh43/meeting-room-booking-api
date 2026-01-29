from datetime import datetime
from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    room_id: str = Field(..., example="room-101")
    start_time: datetime
    end_time: datetime


class Booking(BookingCreate):
    booking_id: str
