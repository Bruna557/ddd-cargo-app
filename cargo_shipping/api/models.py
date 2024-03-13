"""API's request and response types definition."""

from datetime import datetime

from pydantic import BaseModel


class LocationRequest(BaseModel):
    """Location request type definition."""

    code: str
    name: str


class BookingRequest(BaseModel):
    """Booking request type definition."""

    tracking_id: str
    destination: LocationRequest
    deadline: datetime


class HandlingEventRequest(BaseModel):
    """Handling event request type definition."""

    tracking_id: str
    departure_location: LocationRequest
    arrival_location: LocationRequest
    time_stamp: datetime
    event_type: str
