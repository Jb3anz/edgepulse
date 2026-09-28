"""Fault isolation: one failing collector must not crash the agent."""

import logging
from typing import Callable, TypeVar

T = TypeVar("T")

logger = logging.getLogger("edgepulse.collector")


def collect_safely(name: str, collector: Callable[[], T], default: T) -> T:
    """Run `collector`; on any exception log it and return `default`."""
    try:
        return collector()
    except Exception:
        logger.exception("Collector failed: %s", name)
        return default
