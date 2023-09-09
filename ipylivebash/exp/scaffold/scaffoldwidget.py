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
        if isinstance(output, str):
            script = output
            output_widget.clear_output()
            env = {
                "LIVEBASH_VALUE": input,
            }
            task = run_script(script, output_widget.append_stdout, env=env)
            asyncio.get_event_loop().create_task(task)
        elif callable(output):
            output_widget.clear_output()
            output(input, output_widget.append_stdout)
