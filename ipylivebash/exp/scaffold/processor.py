from .inputoutputmixin import IOOptions
from ipylivebash.sessionmanager import run_script
import asyncio


class Processor:
    """
    Process output(s) from input(s) and instance value(s)
    """

    def __init__(self, interface_builder=None, output_widget=None, shared_storage=None):
        self.shared_storage = shared_storage
        self.interface_builder = interface_builder
        self.output_widget = output_widget

    def __call__(self, input, output, value):
        return self.process(input, output, value)

    def process(self, input, output, value):
        self.output_widget.clear_output()
        print_line = (
            self.output_widget.append_stdout if self.output_widget is not None else None
        )
        options = IOOptions(
            source=input,
            shared_storage=self.shared_storage,
            print_line=print_line,
            interface_builder=self.interface_builder,
        )

        if isinstance(output, list):
            outputs = output
        else:
            outputs = [output]

        for target in outputs:
            if isinstance(target, str):
                script = target
                # TODO Handle list type
                env = {
                    "LB_VALUE": value,
                }
                task = run_script(script, print_line=print_line, env=env)
                asyncio.get_event_loop().create_task(task)
            elif callable(target):
                target(value, options)
