import logging
import time
from datetime import datetime, timezone

from client.collectors import cpu, disk, memory, network, system
from client.collectors.safe import collect_safely
from client.config import CLIENT_VERSION, get_collection_interval
from client.identity import get_node_id
from client.models import SCHEMA_VERSION, Telemetry
from client.output import console

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("edgepulse")


def collect_telemetry(node_id: str, network_collector: network.NetworkCollector) -> Telemetry:
    rx, tx, rx_rate, tx_rate = collect_safely(
        "network", network_collector.collect, (0, 0, 0.0, 0.0)
    )

    return Telemetry(
        schema_version=SCHEMA_VERSION,
        node_id=node_id,
        agent_version=CLIENT_VERSION,
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        hostname=system.hostname(),
        platform=system.operating_system(),
        cpu_percent=collect_safely("cpu", cpu.collect, 0.0),
        memory_percent=collect_safely("memory", memory.collect, 0.0),
        disk_percent=collect_safely("disk", disk.collect, 0.0),
        network_rx_bytes=rx,
        network_tx_bytes=tx,
        network_rx_bytes_per_second=rx_rate,
        network_tx_bytes_per_second=tx_rate,
    )


def main() -> None:
    interval = get_collection_interval()
    node_id = get_node_id()  # resolved once, not every cycle
    network_collector = network.NetworkCollector()

    logger.info("EdgePulse client starting (node %s)", node_id)
    logger.info("collection interval: %.1f seconds", interval)

    try:
        while True:
            started = time.monotonic()
            console.write(collect_telemetry(node_id, network_collector))
            # subtract collection time so the period stays steady
            time.sleep(max(0.0, interval - (time.monotonic() - started)))
    except KeyboardInterrupt:
        logger.info("EdgePulse agent stopped")


if __name__ == "__main__":
    main()
