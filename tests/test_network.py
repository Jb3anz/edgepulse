from types import SimpleNamespace

from client.collectors import network


def test_first_call_has_zero_rate(monkeypatch):
    monkeypatch.setattr(
        network.psutil, "net_io_counters",
        lambda: SimpleNamespace(bytes_recv=100, bytes_sent=50),
    )
    rx, tx, rx_rate, tx_rate = network.NetworkCollector().collect()
    assert (rx, tx, rx_rate, tx_rate) == (100, 50, 0.0, 0.0)


def test_rate_computed_from_delta(monkeypatch):
    counters = iter([
        SimpleNamespace(bytes_recv=100, bytes_sent=100),
        SimpleNamespace(bytes_recv=300, bytes_sent=200),
    ])
    times = iter([10.0, 12.0])
    monkeypatch.setattr(network.psutil, "net_io_counters", lambda: next(counters))
    monkeypatch.setattr(network.time, "monotonic", lambda: next(times))

    c = network.NetworkCollector()
    c.collect()
    _, _, rx_rate, tx_rate = c.collect()
    assert rx_rate == 100.0 and tx_rate == 50.0


def test_counter_reset_never_negative(monkeypatch):
    counters = iter([
        SimpleNamespace(bytes_recv=500, bytes_sent=500),
        SimpleNamespace(bytes_recv=10, bytes_sent=10),
    ])
    times = iter([1.0, 2.0])
    monkeypatch.setattr(network.psutil, "net_io_counters", lambda: next(counters))
    monkeypatch.setattr(network.time, "monotonic", lambda: next(times))

    c = network.NetworkCollector()
    c.collect()
    _, _, rx_rate, tx_rate = c.collect()
    assert rx_rate == 0.0 and tx_rate == 0.0
