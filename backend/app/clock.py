"""PROVIDED. Do not modify."""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Timezone-aware current time. Use this rather than `datetime.now()`."""
    return datetime.now(timezone.utc)
