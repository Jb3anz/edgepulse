import psutil


def collect() -> float:
    """Virtual memory usage percentage."""
    return psutil.virtual_memory().percent
