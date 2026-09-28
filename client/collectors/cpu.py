import psutil


def collect() -> float:
    """CPU utilisation percentage sampled over 0.5 seconds."""
    return psutil.cpu_percent(interval=0.5)
