from ipywidgets import widgets
from .iounit.iounit import InputUnit


class WidgetWrapper:
    def __init__(self, widget, container, get_value=None, on_click=None):
        self.widget = widget
        self.container = container
        self.get_value = get_value
        self.on_click = on_click

    def focus(self):
        self.widget.focus()


class WidgetFactory:
    def create_link_button(self, description):
        style = """
        <style>
        .ipylivebash-link-button {
            background: transparent;
            color: #1976d2;
            width: auto;
        }

        .ipylivebash-link-button:hover {
            background: transparent;
            border: none;
            box-shadow: none ! important;
            opacity: 0.5;
        }

        .ipylivebash-link-button:active {
            background: transparent;
            border: none;
            box-shadow: none ! important;
            opacity: 0.7;
        }

        .ipylivebash-link-button:focus {
            border: none;
            box-shadow: none ! important;
            outline: none ! important;
        }
        </style>
        """
        style_html = widgets.HTML(style)

        button = widgets.Button(description=description)
        button.add_class("ipylivebash-link-button")
        container = widgets.Box([button, style_html])

        return WidgetWrapper(
            button, container, on_click=lambda callback: button.on_click(callback)
        )

    def create_input(self, input: InputUnit):
        value = str(input) if input is not None else None

        format = input.format

        is_select = input is not None and isinstance(format.select, list)

        is_textarea = not is_select and (
            format.multiline is True
            or (isinstance(format.multiline, int) and format.multiline > 1)
        )

        if is_select:
            if value not in format.select:
                if input.defaults in format.select:
                    value = input.defaults
                else:
                    value = None
            input_widget = widgets.Select(options=format.select, value=value)
        elif is_textarea:
            rows = format.multiline if not isinstance(format.multiline, bool) else 5
            input_widget = widgets.Textarea(value=value, rows=rows)
        else:
            layout = widgets.Layout(width="240px")
            input_widget = widgets.Text(value=value, layout=layout)

        return WidgetWrapper(
            input_widget, input_widget, get_value=lambda: input_widget.value
        )

    def create_submit_area(self, _output, on_submit, default_label="Submit"):
        # TODO - Handle multiple actions
        submit_button = widgets.Button(description=default_label)

        def button_callback(_):
            on_submit()

        submit_button.on_click(button_callback)

        return (submit_button, submit_button)  # hbox, confirm_button
