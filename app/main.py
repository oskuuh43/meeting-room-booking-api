from fastapi import FastAPI
from app.routes import router as booking_router

app = FastAPI(
    title="Meeting Room Booking API",
    description="Backend API for managing meeting room bookings",
    version="1.0.0"
)

app.include_router(booking_router)
