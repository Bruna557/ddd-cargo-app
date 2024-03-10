from datetime import datetime

from pydantic import BaseModel

from cargo_shipping.domain.model.handling.handling_event import (
    HandlingActivity,
)


class Location(BaseModel):
    name: str
    code: str


class BookingRequest(BaseModel):
    tracking_id: str
    destination: Location
    deadline: datetime


class HandlingEventRequest(BaseModel):
    tracking_id: str
    departure_location: Location
    arrival_location: Location
    time_stamp: datetime
    handling_activity: HandlingActivity
