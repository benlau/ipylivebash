from ..logview import LogView


def test_logview_creation_blank():
    w = LogView()
    assert w.messages == []
