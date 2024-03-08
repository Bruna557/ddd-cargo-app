from app.routers import booking, handling, tracking
from fastapi import FastAPI

app = FastAPI()


app.include_router(booking.router)
app.include_router(handling.router)
app.include_router(tracking.router)
