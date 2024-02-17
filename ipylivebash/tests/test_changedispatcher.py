from ..exp.scaffold.services.changedispatcher import ChangeDispatcher, Listener
from unittest.mock import Mock


def test_listen():
    listener = Mock()
    dispatcher = ChangeDispatcher()
    dispatcher.add_listener(listener)
    dispatcher.dispatch("test", "payload")
    listener.assert_called_with("test", "payload")
