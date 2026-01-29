from datetime import datetime
from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    room_id: str = Field(
        ...,
        description="Identifier of the meeting room",
        example="room-101",
        min_length=1,
    )
    start_time: datetime = Field(
        ...,
        description="Booking start time",
        example="2026-03-01T10:00:00Z",
    )
    end_time: datetime = Field(
        ...,
        description="Booking end time",
        example="2026-03-01T11:00:00Z",
    )


class Booking(BookingCreate):
    booking_id: str = Field(
        ...,
        description="Unique identifier for the booking",
        example="a3f5c2e4-8f2d-4c8a-bc1a-1b2e3f4d5c6a",
    )