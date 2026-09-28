"""Console output sink: prints telemetry as JSON."""

import json

from client.models import Telemetry


def write(telemetry: Telemetry) -> None:
    print(json.dumps(telemetry.to_dict(), indent=2))
