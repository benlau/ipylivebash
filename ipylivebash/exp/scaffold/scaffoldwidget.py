from ipylivebash.sessionmanager import run_script  # noqa
import asyncio
from .doublebufferoutput import DoubleBufferOutput


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
