from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from .scaffoldwidget import ScaffoldWidget, preset_iot_init
from ipywidgets import widgets
from .widgetfactory import WidgetFactory
from .processor import Processor


class SingleValueLayout(ScaffoldWidget):
    @preset_iot_init
    def __init__(self, input=None, output=None, title=None):
        self.input = input
        self.title = title
        self.output = output
        self.action_label = "Confirm"
        self.processor = Processor()

    def create_ipywidget(self):
        layout = []
        factory = WidgetFactory()

        title_widget = None
        if self.title is not None:
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        # confirm_button = widgets.Button(description=self.action_label)
        output_area = DoubleBufferOutput()

        input_widget = factory.create_input(self.input)

        def on_submit():
            self.processor(self.input, self.output, input_widget.value, output_area)

        submit_area = factory.create_submit_area(
            self.output, on_submit=on_submit, default_label=self.action_label
        )

        widgets_box = widgets.VBox(
            layout + [input_widget, submit_area, output_area.vbox]
        )

        return widgets_box
