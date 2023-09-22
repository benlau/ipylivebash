from .inputoutputmixin import InputOutputOptions
from ipylivebash.sessionmanager import run_script
import asyncio


class Processor:
    """
    Process output(s) from input(s) and instance value(s)
    """

    def __init__(self):
        self.shared_storage = {}

    def __call__(self, input, output, value, output_widget):
        return self.process(input, output, value, output_widget)

    def process(self, input, output, value, output_widget):
        output_widget.clear_output()
        options = InputOutputOptions(
            source=input,
            shared_storage=self.shared_storage,
            print_line=output_widget.append_stdout,
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
                task = run_script(
                    script, print_line=output_widget.append_stdout, env=env
                )
                asyncio.get_event_loop().create_task(task)
            elif callable(target):
                target(value, options)
