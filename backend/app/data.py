"""Mock fleet: 26 devices across 4 sites.

PROVIDED. Do not modify.

`last_seen_at` is stored as an offset in seconds and resolved against the
request time. A device that is 45 seconds stale stays 45 seconds stale for the
whole session instead of drifting while you work.
"""

import math
import random
from datetime import datetime, timedelta

from .models import Device, DeviceStatus, Reading, Site

SITES: list[Site] = [
    Site(id="site-atx", name="Barton Creek Plaza", location="Austin, TX"),
    Site(id="site-phx", name="Deer Valley Distribution", location="Phoenix, AZ"),
    Site(id="site-tpa", name="Ybor Logistics Center", location="Tampa, FL"),
    Site(id="site-reno", name="Sparks Cold Storage", location="Reno, NV"),
]

SITE_NAMES: dict[str, str] = {site.id: site.name for site in SITES}

MINUTE = 60
HOUR = 60 * MINUTE

# id, name, site, firmware, status, seconds since last report,
# battery %, temp °C, humidity %
_FLEET: list[
    tuple[
        str,
        str,
        str,
        str,
        DeviceStatus,
        int,
        int | None,
        float | None,
        float | None,
    ]
] = [
    # fmt: off
    ("dev-atx-01", "Rooftop Unit 1 Supply Air",     "site-atx",  "4.2.1", "online",        45, None, 12.4, 48.2),
    ("dev-atx-02", "Rooftop Unit 1 Return Air",     "site-atx",  "4.2.1", "online",        52, None, 23.1, 44.0),
    ("dev-atx-03", "Rooftop Unit 2 Supply Air",     "site-atx",  "4.1.8", "degraded",  14 * MINUTE,   87, 14.9, 51.3),
    ("dev-atx-04", "Zone 3 Return Air",             "site-atx",  "4.2.1", "online",        38,   64, 22.8, 46.1),
    ("dev-atx-05", "Mechanical Room Ambient",       "site-atx",  "4.2.1", "online",   2 * MINUTE + 10,   41, 27.6, 39.8),
    ("dev-atx-06", "Condenser Bay Ambient",         "site-atx",  "3.9.4", "offline",  5 * HOUR + 12 * MINUTE,    8, 31.2, 35.4),
    ("dev-atx-07", "Lobby Thermostat",              "site-atx",  "4.2.1", "online",   1 * MINUTE, None, 22.2, 47.7),

    ("dev-phx-01", "Rooftop Unit 4 Supply Air",     "site-phx",  "4.2.1", "online",        30, None, 13.8, 22.5),
    ("dev-phx-02", "Rooftop Unit 4 Return Air",     "site-phx",  "4.2.1", "online",        33, None, 26.4, 20.9),
    ("dev-phx-03", "Dock Door 2 Ambient",           "site-phx",  "4.1.8", "degraded", 22 * MINUTE,   55, 34.7, 18.2),
    ("dev-phx-04", "Dock Door 5 Ambient",           "site-phx",  "4.2.1", "online",   1 * MINUTE + 5,    73, 33.9, 19.0),
    ("dev-phx-05", "Server Closet Probe",           "site-phx",  "4.2.1", "online",        48, None, 19.6, 31.4),
    ("dev-phx-06", "Pallet Staging Ambient",        "site-phx",  "3.9.4", "offline",  2 * HOUR + 41 * MINUTE,     3, 38.1, 16.7),
    # Commissioned but has never reported a sample.
    ("dev-phx-07", "Roof Access Ambient",           "site-phx",  "4.2.1", "online",   5 * MINUTE,   12, None, None),

    ("dev-tpa-01", "Walk-in Cooler Probe",          "site-tpa",  "4.2.1", "online",        26, None,  3.4, 78.9),
    ("dev-tpa-02", "Walk-in Freezer Probe",         "site-tpa",  "4.1.8", "degraded",  8 * MINUTE,   91, -17.2, 62.5),
    ("dev-tpa-03", "Loading Bay Ambient",           "site-tpa",  "4.2.1", "online",        55,   68, 29.8, 81.2),
    ("dev-tpa-04", "Office Zone 1 Thermostat",      "site-tpa",  "4.2.1", "online",   1 * MINUTE + 12, None, 23.3, 58.4),
    ("dev-tpa-05", "Office Zone 2 Thermostat",      "site-tpa",  "4.2.1", "online",   1 * MINUTE + 18, None, 24.1, 60.1),
    ("dev-tpa-06", "Chiller Loop Return",           "site-tpa",  "3.9.4", "offline",  18 * HOUR, None, 21.7, 70.3),

    ("dev-reno-01", "Freezer Bay A Probe",          "site-reno", "4.2.1", "online",        40, None, -22.6, 55.0),
    ("dev-reno-02", "Freezer Bay B Probe",          "site-reno", "4.2.1", "online",        44, None, -21.9, 54.2),
    ("dev-reno-03", "Dock Ambient",                 "site-reno", "4.1.8", "degraded", 31 * MINUTE,   19,   4.8, 49.7),
    ("dev-reno-04", "Compressor Room Ambient",      "site-reno", "4.2.1", "online",        58, None,  16.3, 41.5),
    ("dev-reno-05", "Ammonia Line Surface Temp",    "site-reno", "4.2.1", "online",   1 * MINUTE + 30,   82,  -8.4, 44.9),
    ("dev-reno-06", "Yard Gate Ambient",            "site-reno", "3.9.4", "offline",  3 * HOUR + 5 * MINUTE,     0,  -1.2, 63.8),
    # fmt: on
]


def load_devices(now: datetime) -> list[Device]:
    """The whole fleet, with `last_seen_at` resolved against `now`."""
    devices: list[Device] = []
    for (
        device_id,
        name,
        site_id,
        firmware,
        status,
        age_seconds,
        battery_pct,
        temp_c,
        humidity_pct,
    ) in _FLEET:
        last_seen_at = now - timedelta(seconds=age_seconds)
        reading = (
            Reading(
                recorded_at=last_seen_at,
                temp_c=temp_c,
                humidity_pct=humidity_pct,
            )
            if temp_c is not None and humidity_pct is not None
            else None
        )
        devices.append(
            Device(
                id=device_id,
                name=name,
                site_id=site_id,
                site_name=SITE_NAMES[site_id],
                status=status,
                firmware=firmware,
                battery_pct=battery_pct,
                last_seen_at=last_seen_at,
                latest_reading=reading,
            )
        )
    return devices


def sample_readings(
    device_id: str, now: datetime, window_minutes: int = 24 * 60
) -> list[Reading]:
    """A deterministic history for one device, for the sparkline stretch goal.

    One sample every 5 minutes over `window_minutes`, oscillating around the
    device's latest values.
    """
    device = next((d for d in load_devices(now) if d.id == device_id), None)
    if device is None or device.latest_reading is None:
        return []

    base_temp = device.latest_reading.temp_c
    base_humidity = device.latest_reading.humidity_pct
    rng = random.Random(device_id)
    step = 5
    points = max(window_minutes // step, 1)

    readings: list[Reading] = []
    for i in range(points, 0, -1):
        phase = (i / points) * 2 * math.pi
        readings.append(
            Reading(
                recorded_at=now - timedelta(minutes=i * step),
                temp_c=round(base_temp + math.sin(phase) * 1.8 + rng.uniform(-0.3, 0.3), 2),
                humidity_pct=round(
                    base_humidity + math.cos(phase) * 4.0 + rng.uniform(-0.8, 0.8), 2
                ),
            )
        )
    readings.append(device.latest_reading)
    return readings
