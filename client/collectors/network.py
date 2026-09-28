import time

import psutil


class NetworkCollector:
    """Reports cumulative network bytes plus per-second rates.

    Rates are computed from the delta since the previous call. The first
    call (and any counter reset) reports a rate of 0.
    """

    def __init__(self) -> None:
        self.previous_rx: int | None = None
        self.previous_tx: int | None = None
        self.previous_time: float | None = None

    def collect(self) -> tuple[int, int, float, float]:
        counters = psutil.net_io_counters()
        current_rx = counters.bytes_recv
        current_tx = counters.bytes_sent
        current_time = time.monotonic()

        rx_rate = tx_rate = 0.0
        if self.previous_time is not None:
            elapsed = current_time - self.previous_time
            if elapsed > 0:
                rx_rate = max(0, current_rx - self.previous_rx) / elapsed
                tx_rate = max(0, current_tx - self.previous_tx) / elapsed

        self.previous_rx = current_rx
        self.previous_tx = current_tx
        self.previous_time = current_time

        return current_rx, current_tx, rx_rate, tx_rate
