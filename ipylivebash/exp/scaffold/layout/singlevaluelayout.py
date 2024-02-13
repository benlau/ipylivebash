from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from ..decorators import preset_iot_class_method
from ipywidgets import widgets
from ..widgetfactory import WidgetFactory
from ..processor import Processor

# SingleValueLayout is a class that creates a layout for a single input value.


class SingleValueLayout:
    @preset_iot_class_method
    def __init__(
        self, input=None, output=None, title=None, context=None, instant_write=False
    ):
        self.input = input
        self.title = title
        self.output = output
        self.action_label = "Confirm"
        self.context = context
        self.instant_write = instant_write
        self.widget = self._create_ipywidget()

    def focus(self):
        self.input_widget.focus()

    def _create_ipywidget(self):
        layout = []
        factory = WidgetFactory()

        title_widget = None
        if self.title is not None:
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        output_area = DoubleBufferOutput()

        input_widget = factory.create_input(self.input)
        self.input_widget = input_widget

        def on_submit():
            processor = Processor(self.context)
            processor(self.input, self.output, input_widget.get_value())

        if self.instant_write is False:
            submit_area = factory.create_submit_area(
                self.output, on_submit=on_submit, default_label=self.action_label
            )
            widgets_box = widgets.VBox(
                layout + [input_widget.container, submit_area, output_area.widget]
            )
        else:

            def on_change(change):
                if change["type"] == "change" and change["name"] == "value":
                    on_submit()

            self.input_widget.widget.observe(on_change)
            widgets_box = widgets.VBox(
                layout + [input_widget.container, output_area.widget]
            )

        return widgets_box
