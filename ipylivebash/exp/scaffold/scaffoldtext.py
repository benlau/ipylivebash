import ipywidgets as widgets
from IPython.display import display
from .doublebufferoutput import DoubleBufferOutput
from .execute import execute
from .scaffoldwidget import ScaffoldWidget
from .utils import inspect_arg_name


class ScaffoldText(ScaffoldWidget):
    def __init__(
        self,
        input=None,
        output=None,
        title=None,
        placeholder="",
        defaults=None,
        action_label="Confirm",
    ):
        self.input = input
        if output is None:
            self.output = input
        else:
            self.output = output
        if title is not None:
            self.title = title
        elif input is not None:
            self.title = inspect_arg_name(0, "input")
        elif output is not None:
            self.title = inspect_arg_name(1, "output")
        self.placeholder = placeholder
        self.action_label = action_label
        if defaults is not None and not isinstance(defaults, str):
            defaults = str(defaults)
        self.defaults = defaults

    def create_ipywidget(self):
        layout = []
        title_widget = None
        if self.title is not None:
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        value = str(self.input) if self.input is not None else None
        if value is None and self.defaults is not None:
            value = self.defaults

        text = widgets.Text(value=value, placeholder=self.placeholder)
        confirm_button = widgets.Button(description=self.action_label)
        output_area = DoubleBufferOutput()

        def confirm_button_callback(_):
            self.execute(text.value, self.output, output_area)

        confirm_button.on_click(confirm_button_callback)

        widgets_box = widgets.VBox(layout + [text, confirm_button, output_area.vbox])

        return widgets_box


def display_text(
    input=None,
    output=None,
    title=None,
    placeholder="",
    defaults=None,
    action_label="Confirm",
):
    if title is None:
        if input is not None:
            title = inspect_arg_name(0, "input")
        elif output is not None:
            title = inspect_arg_name(1, "output")

    display(
        ScaffoldText(
            input, output, title, placeholder, defaults, action_label
        ).create_ipywidget()
    )
