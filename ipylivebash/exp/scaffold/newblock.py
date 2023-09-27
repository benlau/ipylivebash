from ipylivebash.exp.scaffold.preset_iot import preset_iot_class_method
from .inputoutputmixin import IOOptions, OutputObject


class NewBlock(OutputObject):
    """ "
    NewBlock is a OutputObject for create a new unit
    in Scaffold application
    """

    @preset_iot_class_method
    def __init__(self, input=None, output=None, title=None):
        self.input = input
        self.output = output
        self.title = title

    def write(self, value=None, options: IOOptions = None):
        if options is None:
            return

        if options.interface_builder is None:
            return

        options.interface_builder.ask(
            input=self.input, output=self.output, title=self.title
        )
