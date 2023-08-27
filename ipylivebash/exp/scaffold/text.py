import ipywidgets as widgets
from IPython.display import display
from .doublebufferoutput import DoubleBufferOutput
from .execute import execute


def text(title=None, run=None, value=None, placeholder="", action_label="Confirm"):
    title_widget = None
    if title is not None:
        title_widget = widgets.Label(value=title)

    if value is not None and not isinstance(value, str):
        value = str(value)

    select_widget = widgets.Text(value=value, placeholder=placeholder)
    confirm_button = widgets.Button(description=action_label)
    output_area = DoubleBufferOutput()

    def confirm_button_callback(b):
        execute(run, select_widget.value, output_area)

    confirm_button.on_click(confirm_button_callback)

    widgets_box = widgets.VBox(
        [title_widget, select_widget, confirm_button, output_area.vbox]
    )

    return widgets_box


def display_text(title, run, *args, **kwargs):
    display(text(title, run, *args, **kwargs))
