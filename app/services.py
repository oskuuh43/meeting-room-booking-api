from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from app.models import Booking, BookingCreate
from app.storage import BookingStorage


class BookingService:
    def __init__(self, storage: BookingStorage):
        self.storage = storage

    def create_booking(self, booking_data: BookingCreate) -> Booking:
        self._validate_time_range(booking_data)
        self._validate_not_in_past(booking_data)
        self._validate_no_overlap(booking_data)

        booking = Booking(
            booking_id=str(uuid4()),
            **booking_data.model_dump()
        )

        self.storage.add_booking(booking)
        return booking

    def cancel_booking(self, booking_id: str) -> None:
        removed = self.storage.remove_booking(booking_id)
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

    def list_bookings(self, room_id: str):
        bookings = self.storage.get_bookings_for_room(room_id)
        return sorted(bookings, key=lambda booking: booking.start_time)

    # -----------------------
    # Validation helpers
    # -----------------------

    def _validate_time_range(self, booking: BookingCreate) -> None:
        if booking.start_time >= booking.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start time must be before end time"
            )

    def _validate_not_in_past(self, booking: BookingCreate) -> None:
        now = datetime.now(timezone.utc)

        if booking.start_time < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bookings cannot be created in the past"
            )

    def _validate_no_overlap(self, booking: BookingCreate) -> None:
        existing_bookings = self.storage.get_bookings_for_room(booking.room_id)

        for existing in existing_bookings:
            if self._overlaps(
                booking.start_time,
                booking.end_time,
                existing.start_time,
                existing.end_time,
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Booking time overlaps with an existing booking"
                )

    @staticmethod
    def _overlaps(start1, end1, start2, end2) -> bool:
        return start1 < end2 and end1 > start2
