from ipylivebash.exp.scaffold.processor import Processor
from unittest.mock import MagicMock
import asyncio


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


def test_processor_create_task():
    output = MagicMock()
    processor = Processor()
    done = MagicMock()
    task = processor.create_task("input", output, MagicMock())
    task.add_done_callback(done)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    done.assert_called_once()
