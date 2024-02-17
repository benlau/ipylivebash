from ipylivebash.exp.scaffold.decorators import preset_iot_class_method
from .context import Context
from .iounit.iounit import OutputUnit
from .block import Block


class NextBlock(OutputUnit):
    """
    NewBlock is a OutputUnit for create a new unit
    in Scaffold application
    """

    @preset_iot_class_method
    def __init__(self, input=None, output=None, title=None):
        self.input = input
        self.output = output
        self.title = title

    def write(self, value=None, context: Context = None):
        if context is None:
            return

        if context.interface_builder is None:
            return

        next_content = context.create_next_context(input=self.input, output=self.output)

        block = Block(next_content)
        block.ask(input=self.input, output=self.output, title=self.title)
        block.focus()
