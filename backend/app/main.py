"""Fleet API application wiring.

PROVIDED. Do not modify.

`GET /api/sites` below is already written. The UI needs it, and it shows you the
response conventions this codebase uses. Your work goes in
`app/routers/devices.py`.
"""

import asyncio
import random

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .data import SITES
from .models import Site
from .routers import devices

app = FastAPI(title="Fleet API", version="0.1.0")

# The Vite dev server proxies /api, so CORS is only needed if you hit the API
# directly from a browser tab.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def simulate_network_latency(request: Request, call_next):
    """150-300ms of latency, so loading states are visible in the UI."""
    await asyncio.sleep(random.uniform(0.15, 0.30))
    return await call_next(request)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/sites", response_model=list[Site])
async def list_sites() -> list[Site]:
    return SITES


app.include_router(devices.router)
