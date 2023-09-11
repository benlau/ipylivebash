from ipylivebash.sessionmanager import run_script  # noqa
import asyncio
from .doublebufferoutput import DoubleBufferOutput
from .utils import inspect_arg_name


def preset_iot(func):
    """
    A decorator that preset the input, output, title arguments
    """

    def inner(input=None, output=None, title=None, *args, **kwargs):
        if title is None:
            if input is not None:
                title = inspect_arg_name(0, "input")
            elif output is not None:
                title = inspect_arg_name(1, "output")
        if output is None:
            output = input
        return func(input, output, title, *args, **kwargs)

    return inner


class ScaffoldWidget:
    def execute(self, input, output, output_widget: DoubleBufferOutput):
        if isinstance(output, list):
            outputs = output
        else:
            outputs = [output]

        output_widget.clear_output()

        for target in outputs:
            if isinstance(target, str):
                script = target
                env = {
                    "LIVEBASH_VALUE": input,
                }
                task = run_script(
                    script, print_line=output_widget.append_stdout, env=env
                )
                asyncio.get_event_loop().create_task(task)
            elif callable(target):
                target(input, output_widget.append_stdout)
