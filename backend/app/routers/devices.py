"""YOUR TASK. The fleet listing endpoint.

    GET /api/devices

Query parameters, all optional:

    search        Case-insensitive substring on `name` or `siteName`. Trim
                  it. Empty or whitespace-only means no filter.
    status        One of: online | degraded | offline.
                  Repeatable, so `?status=online&status=degraded` means OR.
    siteId        Exact match against `Device.site_id`.
    staleMinutes  Positive integer. Keep only devices whose `lastSeenAt` is
                  MORE than N minutes old, relative to the request time.
    sort          last_seen_desc (default) | last_seen_asc | name_asc.
    page          1-indexed, positive integer. Default 1.
    pageSize      Positive integer. Default 8. Clamp to 24 if larger, don't
                  reject it.

The validation contract. Be exact here, this is the part that gets hand-waved:

    * `status` or `sort` carrying a value outside its set returns 400.
    * `page`, `pageSize` or `staleMinutes` present but not a positive integer
      returns 400. That covers non-numeric, 0, negative, and decimals like 1.5.
    * An unknown `siteId` returns 200 with an empty `data` array, not a 400.
      Sites are an open set that changes without a deploy. Status and sort are
      closed sets baked into this contract. Be ready to defend that split.
    * A `page` past the last page of results returns 200, an empty `data`
      array, and accurate `total`, `page` and `pageSize`.
    * Pick an error body shape, document it, and use it for every 400.

    FastAPI hands you 422s for free if you declare typed `Query` params. Decide
    whether to lean on that and translate, or validate by hand. Both are
    defensible. Say which you picked and why.

A success response matches `DevicesResponse`:

    {"data": [...], "total": 26, "page": 1, "pageSize": 8,
     "generatedAt": "2026-09-18T15:47:10.307507+00:00"}

`total` counts matches after filtering and before pagination.

Notes:
  * `load_devices(now)` returns the whole fleet. Filter, sort and slice it.
  * Use `utc_now()` for the request clock, and pass the same value everywhere
    in one request so `staleMinutes` and `generatedAt` agree.
  * Middleware in `main.py` already adds the artificial latency.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..clock import utc_now  # noqa: F401  (drop this pragma once you use it)
from ..data import load_devices  # noqa: F401
from ..models import DevicesResponse  # noqa: F401

router = APIRouter(prefix="/api", tags=["devices"])


@router.get("/devices")
async def list_devices() -> JSONResponse:
    # TODO: parse and validate the query parameters
    # TODO: filter by search / status / siteId / staleMinutes
    # TODO: sort
    # TODO: paginate
    # TODO: return a DevicesResponse
    return JSONResponse({"error": "not implemented"}, status_code=501)
