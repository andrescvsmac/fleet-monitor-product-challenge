"""Wire models for the fleet API.

PROVIDED. Do not modify.

Python fields are snake_case, the wire format is camelCase. The alias generator
below converts between them, and FastAPI serializes by alias, so a
`DevicesResponse` goes out as `{"data": [...], "pageSize": 8, ...}`.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

DeviceStatus = Literal["online", "degraded", "offline"]

DEVICE_STATUSES: tuple[DeviceStatus, ...] = ("online", "degraded", "offline")

SortOption = Literal["last_seen_desc", "last_seen_asc", "name_asc"]

SORT_OPTIONS: tuple[SortOption, ...] = (
    "last_seen_desc",
    "last_seen_asc",
    "name_asc",
)


class WireModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Reading(WireModel):
    """A single telemetry sample."""

    recorded_at: datetime
    temp_c: float
    humidity_pct: float


class Device(WireModel):
    id: str
    name: str
    site_id: str
    site_name: str
    status: DeviceStatus
    firmware: str
    battery_pct: int | None  # None means the device is mains-powered
    last_seen_at: datetime
    latest_reading: Reading | None  # None means it has never reported


class Site(WireModel):
    id: str
    name: str
    location: str


class DevicesResponse(WireModel):
    data: list[Device]
    total: int  # matches before pagination
    page: int
    page_size: int
    generated_at: datetime  # server clock, so the UI can render "4m ago"
