from client.config import DEFAULT_INTERVAL, get_collection_interval


def test_default_when_unset(monkeypatch):
    monkeypatch.delenv("EDGEPULSE_INTERVAL", raising=False)
    assert get_collection_interval() == DEFAULT_INTERVAL


def test_valid_value(monkeypatch):
    monkeypatch.setenv("EDGEPULSE_INTERVAL", "2.5")
    assert get_collection_interval() == 2.5


def test_invalid_falls_back(monkeypatch):
    monkeypatch.setenv("EDGEPULSE_INTERVAL", "abc")
    assert get_collection_interval() == DEFAULT_INTERVAL


def test_non_positive_falls_back(monkeypatch):
    monkeypatch.setenv("EDGEPULSE_INTERVAL", "-3")
    assert get_collection_interval() == DEFAULT_INTERVAL
