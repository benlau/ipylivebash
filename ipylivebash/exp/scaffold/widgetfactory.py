from ipywidgets import widgets
from .inputoutputmixin import InputObject


class WidgetFactory:
    def create_input(self, input: InputObject):
        value = str(input) if input is not None else None

        is_select = (
            input is not None
            and isinstance(input.defaults, list)
            and not isinstance(input.defaults, str)
        )

        format = input.format

        is_textarea = not is_select and (
            format.multiline is True
            or (isinstance(format.multiline, int) and format.multiline > 1)
        )

        if is_select:
            if value not in input.defaults:
                value = None
            input_widget = widgets.Select(options=input.defaults, value=value)
        elif is_textarea:
            rows = format.multiline if not isinstance(format.multiline, bool) else 5
            input_widget = widgets.Textarea(value=value, rows=rows)
        else:
            layout = widgets.Layout(width="240px")
            input_widget = widgets.Text(value=value, layout=layout)

        return input_widget

    def create_submit_area(self, _output, on_submit, default_label="Submit"):
        # TODO - Handle multiple actions
        submit_button = widgets.Button(description=default_label)

        def button_callback(_):
            on_submit()

        submit_button.on_click(button_callback)
        return submit_button
