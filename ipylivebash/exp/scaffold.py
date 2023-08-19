import asyncio
import ipywidgets as widgets
from IPython.display import display
from ipylivebash.sessionmanager import run_script  # noqa


def _execute(script_or_callback, value, output_widget):
    if isinstance(script_or_callback, str):
        script = script_or_callback.format(value=value)
        output_widget.clear_output()
        env = {
            "LIVEBASH_VALUE": value,
        }
        task = run_script(script, output_widget.append_stdout, env=env)
        asyncio.get_event_loop().create_task(task)
    elif callable(script_or_callback):
        output_widget.clear_output()
        script_or_callback(value, output_widget.append_stdout)


def select(label=None, options=None, run=None, action_label="Confirm"):
    label_widget = None
    if label is not None:
        label_widget = widgets.Label(value=label)

    select_widget = widgets.Select(options=options)
    confirm_button = widgets.Button(description=action_label)
    output_area = widgets.Output()

    def confirm_button_callback(b):
        value = select_widget.value
        _execute(run, value, output_area)

    confirm_button.on_click(confirm_button_callback)

    widgets_box = widgets.VBox(
        [label_widget, select_widget, confirm_button, output_area]
    )

    return widgets_box


def display_select(label, options, callback, **args):
    display(select(label, options, callback, **args))
