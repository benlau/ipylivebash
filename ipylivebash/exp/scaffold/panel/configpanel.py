from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from ..context import Context
from ipylivebash.exp.scaffold.layout.singlevaluelayout import SingleValueLayout
from ipylivebash.exp.scaffold.layout.formlayout import FormLayout
from ipylivebash.exp.scaffold.decorators import preset_iot_class_method
from IPython.display import display
from ipylivebash.exp.scaffold.views.logger import Logger
from ipywidgets import widgets


class ConfigPanel:
    @preset_iot_class_method
    def __init__(
        self,
        input=None,
        output=None,
        title=None,
        log_view=None,
        context=None,
        instant_write=False,
    ):
        self.input = input
        self.output = output
        self.title = title
        self.widget = None
        self.context = context
        self.log_view = log_view
        self.instant_write = instant_write
        self.is_setup_completed = False

    def setup(self):
        if self.is_setup_completed:
            return

        if self.log_view is None:
            self.log_view = Logger()

        if self.context is None:
            self.context = Context(
                input=self.input,
                output=self.output,
                print_line=self.log_view.append_stdout,
                clear_output=self.log_view.clear_output,
            )

        input = self.input
        output = self.output
        title = self.title

        if isinstance(input, list):
            layout = FormLayout(
                input, output, title, self.context, instant_write=self.instant_write
            )
        else:
            layout = SingleValueLayout(
                input,
                output,
                title,
                context=self.context,
                instant_write=self.instant_write,
            )
        self.layout = layout

        self.widget = widgets.VBox([self.layout.widget, self.log_view.widget])

        self.focus()
        self.is_setup_completed = True

    def show(self):
        if not self.is_setup_completed:
            self.setup()
        display(self.widget)

    def focus(self):
        if self.layout is not None:
            self.layout.focus()
