from ipylivebash.exp.scaffold.iounit.iounit import InputUnit
from ipylivebash.sessionmanager import run_script
import asyncio
from inspect import signature
from ipylivebash.exp.scaffold.services.changedispatcher import change_dispatcher


class Processor:
    """
    Run output(s) from input(s) and instance value(s)
    """

    def __init__(self, context=None):
        self.context = context

    def __call__(self, input, output, value):
        return self.process(input, output, value)

    def process(self, input, output, value):
        if self.context is not None:
            self.context.clear_output()
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
                task = run_script(script, print_line=self.context.print_line, env=env)
                asyncio.get_event_loop().create_task(task)
            elif callable(target):
                sig = signature(target)
                arg_count = len(sig.parameters)

                args = [value, self.context][:arg_count]
                target(*args)

                if isinstance(target, InputUnit):
                    object_id = target.get_id()
                    change_dispatcher.dispatch(object_id, value)

    def create_task(self, input, output, value):
        async def run():
            return self.process(input, output, value)

        return asyncio.get_event_loop().create_task(run())
