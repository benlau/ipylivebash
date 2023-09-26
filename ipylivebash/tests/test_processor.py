from ipylivebash.exp.scaffold.processor import Processor


def test_processor_skip_options():
    processor = Processor()

    def callback(value):
        assert value == "test"

    processor(input=None, output=callback, value="test")
