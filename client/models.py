"""Telemetry payload schema.

A dataclass is used instead of hand-built dicts so new fields only need to
be added in one place; `to_dict()` picks them up automatically.
"""

from dataclasses import dataclass, asdict
from typing import Any

SCHEMA_VERSION = "1.0"


@dataclass
class Telemetry:
    schema_version: str
    node_id: str
    agent_version: str
    timestamp: str
    hostname: str
    platform: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_rx_bytes: int
    network_tx_bytes: int
    network_rx_bytes_per_second: float
    network_tx_bytes_per_second: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
