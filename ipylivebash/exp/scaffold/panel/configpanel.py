from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from ..context import Context
from ..singlevaluelayout import SingleValueLayout
from ..formlayout import FormLayout
from IPython.display import display
from ipywidgets import widgets


class ConfigPanel:
    def __init__(
        self, input=None, output=None, title=None, log_view=None, context=None
    ):
        self.input = input
        self.output = output
        self.title = title
        self.widget = None
        self.context = None

        if log_view is not None:
            self.log_view = log_view
        else:
            self.log_view = DoubleBufferOutput()

        self.is_setup_completed = False

    def setup(self):
        if self.is_setup_completed:
            return

        if self.context is None:
            self.context = Context(
                input=self.input,
                output=self.output,
                print_line=self.log_view.append_stdout,
            )

        input = self.input
        output = self.output
        title = self.title

        if isinstance(input, list):
            layout = FormLayout(input, output, title, self.context)
        else:
            layout = SingleValueLayout(input, output, title, self.context)
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
