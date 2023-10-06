from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from ipylivebash.exp.scaffold.decorators import preset_iot_class_method
from .interfacebuilder import InterfaceBuilder
from .singlevaluelayout import SingleValueLayout
from .formlayout import FormLayout
from .columnflow import ColumnFlow
from .context import Context
from IPython.display import display, clear_output
from ipywidgets import widgets


class Block(InterfaceBuilder):
    def __init__(self, context):
        self.context = context

    def ask(self, input=None, output=None, title=None):
        self.context.column_flow.truncate(self.context.current_block_index)
        if isinstance(input, list):
            layout = FormLayout(input, output, title, self.context)
        else:
            layout = SingleValueLayout(input, output, title, self.context)
        self.layout = layout
        self.context.column_flow.append(layout.widget)
        self.focus()

        return {
            "input": input,
            "output": output,
            "title": title,
            "layout": layout,
        }

    def focus(self):
        self.layout.focus()


class Scaffold(InterfaceBuilder):
    """
    The Scaffold provides a framework build interface
    for configuration and task execution quickly.
    """

    def __init__(self):
        pass

    @preset_iot_class_method
    def ask(self, input=None, output=None, title=None):
        shared_storage = {}
        output_widget = DoubleBufferOutput()
        column_flow = ColumnFlow()
        vbox = widgets.VBox([column_flow.widget, output_widget.widget])

        context = Context(
            shared_storage=shared_storage,
            input=input,
            output=output,
            column_flow=column_flow,
            print_line=output_widget.append_stdout,
            clear_output=output_widget.clear_output,
        )

        clear_output()
        display(vbox)
        block = Block(context)
        block.ask(input, output, title)
        block.focus()
