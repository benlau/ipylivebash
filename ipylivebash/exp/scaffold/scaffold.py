from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from ipylivebash.exp.scaffold.preset_iot import preset_iot_class_method
from .interfacebuilder import InterfaceBuilder
from .singlevaluelayout import SingleValueLayout
from .formlayout import FormLayout
from .columnflow import ColumnFlow
from .processor import Processor
from IPython.display import display, clear_output
from ipywidgets import widgets


class _ScaffoldInterfaceBuilder(InterfaceBuilder):
    def __init__(self, index, shared_storage, flow, output_widget):
        self.index = index
        self.flow = flow
        self.output_widget = output_widget
        self.shared_storage = shared_storage

    @preset_iot_class_method
    def ask(self, input=None, output=None, title=None):
        self.flow.truncate(self.index)
        if isinstance(input, list):
            layout = FormLayout(input, output, title)
        else:
            layout = SingleValueLayout(input, output, title)
        layout.processor = Processor(
            interface_builder=_ScaffoldInterfaceBuilder(
                self.index + 1, self.shared_storage, self.flow, self.output_widget
            ),
            output_widget=self.output_widget,
            shared_storage=self.shared_storage,
        )
        self.layout = layout
        self.flow.append(layout.widget)
        self.focus()

    def focus(self):
        self.layout.focus()


class Scaffold(InterfaceBuilder):
    """
    The Scaffold provides a framework build interface
    for configuration and task execution quickly.
    """

    def __init__(self):
        self.shared_storage = {}

    @preset_iot_class_method
    def ask(self, input=None, output=None, title=None):
        output_widget = DoubleBufferOutput()

        flow = ColumnFlow()

        vbox = widgets.VBox([flow.widget, output_widget.widget])

        clear_output()
        display(vbox)
        _delegate = _ScaffoldInterfaceBuilder(
            0, self.shared_storage, flow, output_widget
        )
        _delegate.ask(input, output, title)
        _delegate.focus()
