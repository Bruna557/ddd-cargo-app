"""FastAPI entry point."""

from fastapi import FastAPI

from cargo_shipping.app.routers import booking, handling, tracking

app = FastAPI()


app.include_router(booking.router)
app.include_router(handling.router)
app.include_router(tracking.router)
