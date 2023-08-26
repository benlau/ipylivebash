import asyncio
import ipywidgets as widgets
from IPython.display import display
import os
from ipylivebash.sessionmanager import run_script  # noqa


class EnvVar:
    """
    Wrapper for environment variable
    """

    def __init__(self, name):
        self.name = name

    def __call__(self, value, output):
        os.environ[self.name] = value
        output(f"Set {self.name}={value}")


def _execute(script_or_callback, value, output_widget):
    if isinstance(script_or_callback, str):
        script = script_or_callback
        output_widget.clear_output()
        env = {
            "LIVEBASH_VALUE": value,
        }
        task = run_script(script, output_widget.append_stdout, env=env)
        asyncio.get_event_loop().create_task(task)
    elif callable(script_or_callback):
        output_widget.clear_output()
        script_or_callback(value, output_widget.append_stdout)


def select(title=None, options=None, run=None, action_label="Confirm"):
    title_widget = None
    if title is not None:
        title_widget = widgets.Label(value=title)

    select_widget = widgets.Select(options=options)
    confirm_button = widgets.Button(description=action_label)
    output_area = widgets.Output()

    def confirm_button_callback(b):
        value = select_widget.value
        _execute(run, value, output_area)

    confirm_button.on_click(confirm_button_callback)

    widgets_box = widgets.VBox(
        [title_widget, select_widget, confirm_button, output_area]
    )

    return widgets_box


def display_select(title, options, run, **args):
    """
    Show a select widget

    Parameters
    ----------
    title: str
        Title of the widget

    options: list
        List of options(string)

    run: str or callable
    """
    display(select(title, options, run, **args))
