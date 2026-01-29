from fastapi import APIRouter, status
from typing import List

from app.models import Booking, BookingCreate
from app.services import BookingService
from app.storage import BookingStorage

router = APIRouter(prefix="/api")

# Shared in-memory storage & service
storage = BookingStorage()
service = BookingService(storage)


@router.post(
    "/bookings",
    response_model=Booking,
    status_code=status.HTTP_201_CREATED
)
def create_booking(booking: BookingCreate):
    return service.create_booking(booking)


@router.delete(
    "/bookings/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def cancel_booking(booking_id: str):
    service.cancel_booking(booking_id)


@router.get(
    "/rooms/{room_id}/bookings",
    response_model=List[Booking]
)
def list_bookings(room_id: str):
    return service.list_bookings(room_id)
