from typing import List
from .scaffoldwidget import ScaffoldWidget
import ipywidgets as widgets
from IPython.display import display
from .scaffoldvar import ScaffoldVar
from .doublebufferoutput import DoubleBufferOutput


class Form(ScaffoldWidget):
    def __init__(self, input: List[ScaffoldVar], title="Form"):
        if isinstance(input, list):
            self.input = input
        else:
            self.input = [input]
        self.title = title

    def create_ipywidget(self):
        output_area = DoubleBufferOutput()

        def on_update_text(input):
            def callback(changes):
                value = changes["new"]
                input.write(value)

            return callback

        layout = []
        title_widget = None
        if self.title is not None:
            title_widget = widgets.Label(value=self.title)
            layout.append(title_widget)

        grid = widgets.GridspecLayout(len(self.input), 2)

        grid._grid_template_columns = (
            "auto 1fr"  # A dirty hack to override the default value
        )

        for i, input in enumerate(self.input):
            label = widgets.Label(
                value=input.key, layout=widgets.Layout(margin_right="20px")
            )
            label.layout.margin = "0px 20px 0px 0px"
            text = widgets.Text(value=str(input), placeholder="")
            grid[i, 0] = label
            grid[i, 1] = text
            text.observe(on_update_text(input), names="value")

        widgets_box = widgets.VBox(layout + [grid, output_area.vbox])
        return widgets_box
