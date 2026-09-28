import os

import psutil


def collect() -> float:
    """Disk usage percentage of the root filesystem."""
    path = os.path.abspath(os.sep)
    return psutil.disk_usage(path).percent
