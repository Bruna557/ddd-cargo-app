from datetime import datetime

from pydantic import BaseModel


class LocationRequest(BaseModel):
    code: str
    name: str


class BookingRequest(BaseModel):
    tracking_id: str
    destination: LocationRequest
    deadline: datetime


class HandlingEventRequest(BaseModel):
    tracking_id: str
    departure_location: LocationRequest
    arrival_location: LocationRequest
    time_stamp: datetime
    handling_activity: str
