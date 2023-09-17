from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from .scaffoldwidget import ScaffoldWidget, preset_iot_init
from ipywidgets import widgets


class SingleValueLayout(ScaffoldWidget):
    @preset_iot_init
    def __init__(self, input=None, output=None, title=None):
        self.input = input
        self.title = title
        self.output = output
        self.action_label = "Confirm"

    def create_ipywidget(self):
        layout = []
        title_widget = None
        if self.title is not None:
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        value = str(self.input) if self.input is not None else None

        confirm_button = widgets.Button(description=self.action_label)
        output_area = DoubleBufferOutput()

        if (
            self.input is not None
            and isinstance(self.input.defaults, list)
            and not isinstance(self.input.defaults, str)
        ):
            input_widget = widgets.Select(options=self.input.defaults, value=value)
        else:
            input_widget = widgets.Text(value=value)

        def confirm_button_callback(_):
            self.execute(input_widget.value, self.output, output_area)

        confirm_button.on_click(confirm_button_callback)

        widgets_box = widgets.VBox(
            layout + [input_widget, confirm_button, output_area.vbox]
        )

        return widgets_box
