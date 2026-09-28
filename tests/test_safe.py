from client.collectors.safe import collect_safely


def test_returns_value_on_success():
    assert collect_safely("ok", lambda: 42.0, 0.0) == 42.0


def test_returns_default_on_failure():
    def boom():
        raise RuntimeError("fail")

    assert collect_safely("bad", boom, -1.0) == -1.0
