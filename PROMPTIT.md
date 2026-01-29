# AI työkalun valinta

Tälle projektille päätin käyttää ChatGPT AI-työkalua



## Prompti 1

I want you to help me implement a meeting room booking API using Python and FastAPI. The goal is to Implement a backend-only API that allows clients to manage bookings for meeting rooms.

Implement an API that supports: 
1. Creating a booking for a specific room and time interval. 
2. Cancelling existing bookings. 
3. Listing all bookings for a specific room. 

Business rules (Must be enforced): 
- Bookings for the same room cannot overlap in time 
- Bookings cannot be created in the past 
- The booking start time must be before the end time

Technical constraints: 
- Use Python and FastAPI. 
- Use in-memory storage only (no database needed) 
- Backend only (no frontend needed) 
- Rooms can be identified by a simple "room_id" 
- Authentication and multiple users are not needed in the application

Please walk me through the implementation step by step, starting with setting up the project and proposing a clean and simple project structure.

I will be using PyCharm as my coding environment.

## ChatGPT Vastaus 1
Nice, this is a great little API to build—clean scope, real-world rules 👍
I’ll walk you through this step by step, like we’re pairing on it. We’ll keep things simple, readable, and FastAPI-idiomatic, and I’ll explain why we’re doing each thing.

We’ll start today with project setup + structure, then move gradually into models, storage, and endpoints.

### Step 1: Create the project & virtual environment
1. Create a new PyCharm project

In PyCharm:

1. New Project

2. Choose Pure Python

3. Name it something like:

meeting-room-booking-api


4. Select New virtual environment (recommended)

5. Python 3.10+ is ideal

Once created, you should have something like:

meeting-room-booking-api/

2. Install dependencies

Open the PyCharm terminal (bottom panel) and run:

pip install fastapi uvicorn


We’ll use:

- FastAPI → API framework

- Uvicorn → ASGI server to run the app

### Step 2: Propose a clean project structure

Since this is backend-only and in-memory, we don’t need anything fancy—but we do want clean separation.

Here’s a simple, scalable structure:

meeting-room-booking-api/
│
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # Pydantic models (request/response)
│   ├── storage.py           # In-memory data storage
│   ├── services.py          # Business logic (booking rules)
│   └── routes.py            # API endpoints
│
├── requirements.txt
└── README.md

Why this structure?

- main.py – bootstraps the app

- models.py – defines booking schemas (clean validation)

- storage.py – isolates in-memory storage (easy to replace later)

- services.py – enforces business rules (no overlaps, no past bookings)

- routes.py – thin API layer, easy to read & test

This is much cleaner than putting everything in one file, but still very approachable.

### Step 3: Create the FastAPI app entry point

Create the file:

app/main.py

main.py
from fastapi import FastAPI
from app.routes import router as booking_router

app = FastAPI(
    title="Meeting Room Booking API",
    description="Backend API for managing meeting room bookings",
    version="1.0.0"
)

app.include_router(booking_router)


This file does just one thing:

- Creates the FastAPI app

- Registers the routes

### Step 4: Verify the app runs

From the project root, run:

uvicorn app.main:app --reload


You should see something like:

Uvicorn running on http://127.0.0.1:8000


Now open your browser and visit:

- Swagger UI → http://127.0.0.1:8000/docs

- ReDoc → http://127.0.0.1:8000/redoc

Even though we haven’t added endpoints yet, this confirms:
✅ FastAPI is installed
✅ Project structure works
✅ PyCharm setup is good

### Step 5: Define the booking data model

Next, we define what a booking looks like.

Create:

app/models.py

models.py
from datetime import datetime
from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    room_id: str = Field(..., example="room-101")
    start_time: datetime
    end_time: datetime


class Booking(BookingCreate):
    booking_id: str

Why two models?

- BookingCreate → what the client sends

- Booking → what the API stores & returns

FastAPI + Pydantic automatically:

- Parses ISO 8601 datetime strings

- Validates input

- Generates Swagger docs

What we’ll do next (roadmap)

If you’re good with this so far, next steps will be:

1. In-memory storage (simple dictionary)

2. Business logic

- No overlaps

- No past bookings

- Start < end

3. API routes

- Create booking

- Cancel booking

- List bookings by room

4. Error handling & clean responses

5. Manual testing via Swagger

👉 Next step suggestion:

Shall we implement in-memory storage + booking overlap logic next? That’s where the real fun begins 😄



## Prompti 2

you forgot to define the router in the routes.py file. went ahead and added this to the file:

from fastapi import APIRouter

router = APIRouter()

I have now added everything you sent so far, and the URL:s http://127.0.0.1:8000/docs and http://127.0.0.1:8000/redoc are working. 

Lets move on with the next step.
Please implement the in-memory storage and business logic for managing bookings:
- Storing bookings per room
- Preventing overlapping bookings
- validating that bookings are not in the past
- ensuring start time is before end time



## ChatGPT Vastaus 2

Nice catch on the router 👌 — and perfect, you’re exactly where we want to be.
Now we’re moving into the core of the system: storage + business rules.

We’ll do this cleanly and deliberately so:

- rules live in one place

- API routes stay thin

- logic is easy to test and reason about

### Step 6: In-memory storage design
What we need

We want to:

Store bookings per room

Retrieve bookings by room

Add & remove bookings

A dictionary of lists is perfect:

{
  "room-101": [Booking, Booking, ...],
  "room-202": [Booking, ...]
}


No database, no persistence — simple and fast.

### Step 7: Implement in-memory storage

Create:

app/storage.py

storage.py
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

Why this works well

- Storage logic is isolated

- Easy to swap with a database later

- No FastAPI dependency here → pure Python

### Step 8: Business logic (the rules)

Now we enforce all booking constraints in one place.

Business rules recap

We must enforce:

1. Start time before end time

2. Booking is not in the past

3. Bookings for the same room cannot overlap

### Step 9: Implement booking service (business logic)

Create:

app/services.py

services.py
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
        return self.storage.get_bookings_for_room(room_id)

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

### Step 10: Why this overlap logic is correct

This condition:

start1 < end2 and end1 > start2


Catches all overlap cases:

- Partial overlap

- One booking fully inside another

- Exact edge collision (except end == start, which we allow)

This is the standard, correct interval overlap formula.

### Step 11: What we’ve achieved so far

At this point, you have:

✅ In-memory storage
✅ Centralized business logic
✅ All rules enforced
✅ Clean separation of concerns
✅ No FastAPI leakage into storage

What’s missing (and coming next):

➡️ API endpoints that call this service:

- POST /bookings

- DELETE /bookings/{booking_id}

- GET /rooms/{room_id}/bookings

Next step (recommended)

Next, we’ll:

- Wire routes → service → storage

- Return proper HTTP responses

- Test everything via Swagger

👉 Ready to implement the API routes next?


## Prompti 3
I added the code to the project. lets move on with the next step.




## ChatGPT Vastaus 3
Perfect — you’re moving at exactly the right pace 👍
Now we’ll wire everything together by adding the API endpoints. This is the last big functional step, and it’ll immediately make your Swagger UI come alive.

Step 12: Initialize shared storage & service

Because we’re using in-memory storage, we need one shared instance for the whole app.

We’ll create it in routes.py so:

- It lives as long as the app runs

- All requests see the same data

Step 13: Implement API routes

Open:

app/routes.py


Replace its contents with the following.

routes.py
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

Step 14: What these endpoints do
1️⃣ Create a booking
POST /api/bookings


Request body:

{
  "room_id": "room-101",
  "start_time": "2026-02-01T10:00:00Z",
  "end_time": "2026-02-01T11:00:00Z"
}


✔ Validates:

- Not in the past

- Start < end

- No overlap

✔ Returns:

{
  "booking_id": "uuid",
  "room_id": "room-101",
  "start_time": "...",
  "end_time": "..."
}

2️⃣ Cancel a booking
DELETE /api/bookings/{booking_id}


✔ Returns:

- 204 No Content if successful

- 404 Not Found if booking doesn’t exist

3️⃣ List bookings for a room
GET /api/rooms/{room_id}/bookings


✔ Returns:

[
  {
    "booking_id": "...",
    "room_id": "room-101",
    "start_time": "...",
    "end_time": "..."
  }
]

Step 15: Test everything in Swagger

Restart the server if needed:

uvicorn app.main:app --reload


Go to:
👉 http://127.0.0.1:8000/docs

Suggested test flow:

1. Create a booking

2. Try overlapping → expect 409

3. Try past date → expect 400

4. List bookings for the room

5. Cancel booking

6. Cancel again → expect 404

Step 16: Final sanity checklist

You now have:

✅ FastAPI backend
✅ In-memory booking storage
✅ Business rules enforced
✅ Clean project structure
✅ Fully documented API
✅ Zero external dependencies

This is absolutely interview-ready and easy to extend.

Optional next steps (if you want to go further)

We could:

- Add unit tests (pytest)

- Add sorting by start time

- Add room availability endpoint

- Add graceful shutdown hooks

- Discuss thread-safety & scaling implications

👉 Want to polish this further, or are you done for now?





