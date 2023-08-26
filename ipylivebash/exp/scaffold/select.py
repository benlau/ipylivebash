import ipywidgets as widgets
from IPython.display import display
from .doublebufferoutput import DoubleBufferOutput
from .execute import execute


def select(title=None, options=None, run=None, value=None, action_label="Confirm"):
    title_widget = None
    if title is not None:
        title_widget = widgets.Label(value=title)

    if not isinstance(value, str):
        value = str(value)

    if not value in options:
        value = options[0]

    select_widget = widgets.Select(options=options, value=value)
    confirm_button = widgets.Button(description=action_label)
    output_area = DoubleBufferOutput()

    def confirm_button_callback(b):
        value = select_widget.value
        execute(run, value, output_area)

    confirm_button.on_click(confirm_button_callback)

    widgets_box = widgets.VBox(
        [title_widget, select_widget, confirm_button, output_area.vbox]
    )

    return widgets_box


def display_select(title, options, run, *args, **kwargs):
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
    display(select(title, options, run, *args, **kwargs))
