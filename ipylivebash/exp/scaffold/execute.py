import asyncio
from .doublebufferoutput import DoubleBufferOutput
from ipylivebash.sessionmanager import run_script  # noqa


def execute(script_or_callback, value, output_widget: DoubleBufferOutput):
    if isinstance(script_or_callback, str):
        script = script_or_callback
        output_widget.clear_output()
        env = {
            "LIVEBASH_VALUE": value,
        }
        task = run_script(script, output_widget.append_stdout, env=env)
        asyncio.get_event_loop().create_task(task)
    elif callable(script_or_callback):
        output_widget.clear_output()
        script_or_callback(value, output_widget.append_stdout)
