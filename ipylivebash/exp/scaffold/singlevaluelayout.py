from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from .preset_iot import preset_iot_class_method
from ipywidgets import widgets
from .widgetfactory import WidgetFactory
from .processor import Processor


class SingleValueLayout:
    @preset_iot_class_method
    def __init__(self, input=None, output=None, title=None):
        self.input = input
        self.title = title
        self.output = output
        self.action_label = "Confirm"
        self.processor = Processor()
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
            self.processor(self.input, self.output, input_widget.value)

        submit_area = factory.create_submit_area(
            self.output, on_submit=on_submit, default_label=self.action_label
        )

        widgets_box = widgets.VBox(
            layout + [input_widget, submit_area, output_area.widget]
        )

        return widgets_box
