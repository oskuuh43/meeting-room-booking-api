from typing import Dict, List
from app.models import Booking


class BookingStorage:
    def __init__(self):
        # room_id -> list of bookings
        self._bookings: Dict[str, List[Booking]] = {}

    def get_bookings_for_room(self, room_id: str) -> List[Booking]:
        return self._bookings.get(room_id, [])

    def add_booking(self, booking: Booking) -> None:
        if booking.room_id not in self._bookings:
            self._bookings[booking.room_id] = []
        self._bookings[booking.room_id].append(booking)

    def remove_booking(self, booking_id: str) -> bool:
        for room_bookings in self._bookings.values():
            for booking in room_bookings:
                if booking.booking_id == booking_id:
                    room_bookings.remove(booking)
                    return True
        return False
