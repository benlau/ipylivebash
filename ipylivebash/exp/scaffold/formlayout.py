from typing import List
from .scaffoldwidget import ScaffoldWidget, preset_iot_class_method
import ipywidgets as widgets
from IPython.display import display
from .scaffoldvar import ScaffoldVar
from .doublebufferoutput import DoubleBufferOutput
from .widgetfactory import WidgetFactory
from .inputoutputmixin import OutputObject
from .processor import Processor


class ApplyToSource(OutputObject):
    def __call__(self, value, options):
        values = []
        sources = []
        if isinstance(value, list):
            values = value
            sources = options.source
        else:
            values = [value]
            sources = [options.source]

        for index, value in enumerate(values):
            source = sources[index]
            source.write(value, options)


class FormLayout(ScaffoldWidget):
    def __init__(self, input: List[ScaffoldVar], output=None, title="Form"):
        if isinstance(input, list):
            self.input = input
        else:
            self.input = [input]
        if output is None:
            output = ApplyToSource()
        self.title = title
        self.output = output
        self.widget = self._create_ipywidget()

    def _create_ipywidget(self):
        factory = WidgetFactory()
        output_widget = DoubleBufferOutput()

        layout = []
        title_widget = None
        if self.title is not None:
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        grid = widgets.GridspecLayout(len(self.input), 2)

        grid._grid_template_columns = (
            "auto 1fr"  # A dirty hack to override the default value
        )
        grid._grid_template_rows = "auto"

        for i, input in enumerate(self.input):
            label = widgets.Label(
                value=input.key, layout=widgets.Layout(margin_right="20px")
            )
            label.layout.margin = "0px 20px 0px 0px"

            input_widget = factory.create_input(input)
            grid[i, 0] = label
            grid[i, 1] = input_widget

        def on_submit():
            values = []
            for i, _ in enumerate(self.input):
                values.append(grid[i, 1].value)

            self.processor(self.input, self.output, values)

        submit_area = factory.create_submit_area(self.output, on_submit)
        widgets_box = widgets.VBox(layout + [grid, submit_area, output_widget.widget])
        return widgets_box
