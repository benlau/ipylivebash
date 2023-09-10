from ipylivebash.exp.scaffold.scaffoldwidget import ScaffoldWidget, preset_iot
import ipywidgets as widgets
from IPython.display import display
from .doublebufferoutput import DoubleBufferOutput


class ScaffoldSelect(ScaffoldWidget):
    def __init__(
        self,
        input=None,
        output=None,
        title=None,
        options=None,
        defaults=None,
        action_label="Confirm",
    ):
        self.input = input
        if output is None:
            self.output = input
        else:
            self.output = output
        self.title = title
        self.options = options
        self.action_label = action_label
        if defaults is not None and not isinstance(defaults, str):
            defaults = str(defaults)
        self.defaults = defaults

    def create_ipywidgets(self):
        layout = []
        title_widget = None
        if self.title is not None:
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        value = str(self.input) if self.input is not None else None
        if value is None and self.defaults is not None:
            value = self.defaults

        select_widget = widgets.Select(options=self.options, value=value)
        confirm_button = widgets.Button(description=self.action_label)
        output_area = DoubleBufferOutput()

        def confirm_button_callback(_):
            self.execute(select_widget.value, self.output, output_area)

        confirm_button.on_click(confirm_button_callback)

        widgets_box = widgets.VBox(
            layout + [select_widget, confirm_button, output_area.vbox]
        )

        return widgets_box


@preset_iot
def display_select(
    input=None,
    output=None,
    title=None,
    options=None,
    defaults=None,
    action_label="Confirm",
):
    """
    Show a select widget

    Parameters
    ----------
    title: str
        Title of the widget

    options: list
        List of options(string)

    run: str or callable or EnvVar
    """
    display(
        ScaffoldSelect(
            input, output, title, options, defaults, action_label
        ).create_ipywidgets()
    )
