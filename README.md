# EdgePulse

A lightweight, fault-tolerant system telemetry agent written in Python. EdgePulse collects CPU, memory, disk, and network metrics from a host on a configurable interval and emits them as a versioned JSON payload, ready to be shipped to a monitoring backend.

## Features

- **Metrics collected:** CPU %, memory %, disk %, network bytes sent/received, and per-second network throughput
- **Fault isolation:** each collector runs behind a safety wrapper, so one failing collector logs an error and falls back to a default instead of crashing the agent
- **Stable node identity:** a UUID is generated on first run and persisted in the OS-appropriate app-data directory (via `platformdirs`), so the same machine reports the same ID across restarts
- **Versioned schema:** payloads carry `schema_version` and `agent_version` for backward-compatible evolution
- **Configurable:** collection interval set through an environment variable, with validation and safe fallback
- **Cross-platform:** Linux, macOS, and Windows
- **Tested:** unit tests for configuration parsing, fault isolation, and network rate calculation

## Architecture

```
client/
├── main.py          # collection loop and payload assembly
├── config.py        # version + environment-driven settings
├── identity.py      # persistent node ID
├── models.py        # Telemetry dataclass (payload schema)
├── collectors/
│   ├── cpu.py  memory.py  disk.py  network.py  system.py
│   └── safe.py      # collect_safely(): error isolation wrapper
└── output/
    └── console.py   # output sink (JSON to stdout)
```

Design notes:

- The payload is a `dataclass` serialised with `asdict`, so adding a metric means adding one field, with no manual dict wiring.
- The network collector is stateful: it stores the previous counter reading and timestamp (using a monotonic clock) to compute throughput, and clamps deltas at zero to survive counter resets.
- The loop subtracts collection time from the sleep so the reporting period stays steady.
- Output sinks are separate from collectors, so adding an HTTP or MQTT sender doesn't touch collection logic.

## Getting started

```bash
git clone https://github.com/<your-username>/edgepulse.git
cd edgepulse
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
edgepulse
```

Or run without installing the entry point:

```bash
python -m client.main
```

### Configuration

| Variable | Default | Description |
|---|---|---|
| `EDGEPULSE_INTERVAL` | `5.0` | Seconds between collections. Invalid or non-positive values fall back to the default. |

```bash
EDGEPULSE_INTERVAL=2 edgepulse
```

### Example output

```json
{
  "schema_version": "1.0",
  "node_id": "3f2b8c1e-9a4d-4e7b-b1c2-5d6e7f8a9b0c",
  "agent_version": "0.1.0",
  "timestamp": "2026-09-28T12:00:00Z",
  "hostname": "my-laptop",
  "platform": "Linux",
  "cpu_percent": 12.4,
  "memory_percent": 48.1,
  "disk_percent": 63.7,
  "network_rx_bytes": 1482930211,
  "network_tx_bytes": 302918842,
  "network_rx_bytes_per_second": 20480.5,
  "network_tx_bytes_per_second": 3120.0
}
```

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## Roadmap

- [ ] HTTP output sink to POST telemetry to a collector API
- [ ] Local buffering and retry when the backend is unreachable
- [ ] Ingestion server and dashboard
- [ ] Additional collectors (per-process stats, temperature, load average)
- [ ] GitHub Actions CI

## License

MIT
