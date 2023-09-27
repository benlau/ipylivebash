from ipylivebash.exp.scaffold.processor import Processor
from unittest.mock import MagicMock, call


def test_processor_skip_options():
    processor = Processor()

    def callback(value):
        assert value == "test"

    processor(input=None, output=callback, value="test")


def test_processor_execute_list():
    callback = MagicMock()

    processor = Processor()
    processor("input", [callback, callback], MagicMock())

    assert callback.call_count == 2
