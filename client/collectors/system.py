import platform
import socket


def hostname() -> str:
    return socket.gethostname()


def operating_system() -> str:
    return platform.system()
