"""Configuration: client version and environment-driven settings."""

import os

CLIENT_VERSION = "0.1.0"
DEFAULT_INTERVAL = 5.0


def get_collection_interval() -> float:
    """Return the collection interval in seconds.

    Reads EDGEPULSE_INTERVAL and falls back to the default if the value
    is missing, non-numeric, or not positive.
    """
    value = os.getenv("EDGEPULSE_INTERVAL", str(DEFAULT_INTERVAL))
    try:
        interval = float(value)
    except ValueError:
        return DEFAULT_INTERVAL

    if interval <= 0:
        return DEFAULT_INTERVAL

    return interval
