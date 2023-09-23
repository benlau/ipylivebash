from ipywidgets import widgets
from IPython.display import Javascript
import uuid
import json


class ColumnFlow:
    def __init__(self):
        self.id = uuid.uuid4()
        self.columns = []
        self.hbox = widgets.HBox([])

    @property
    def widget(self):
        return self.hbox

    @property
    def child_count(self):
        return len(self.hbox.children)

    def _create_scroll_to_end_injection(self):
        js = """
        var src = event.target;
        var parent = src.parentNode;
        while (!parent.classList.contains("widget-hbox")) {
            parent = parent.parentNode;
        }
        parent.scrollLeft = parent.scrollWidth;
        """
        escaped_js = js.replace('"', "&quot;")
        div = f"""
        <img src onerror="{escaped_js}"/>
        """
        html = widgets.HTML(div)
        html.layout.display = "none"
        return html

    def _create_container(self, child):
        layout = widgets.Layout(
            min_width="200px",
        )
        injected = self._create_scroll_to_end_injection()
        container = widgets.VBox([injected, child], layout=layout)
        return container

    def append(self, child):
        container = self._create_container(child)
        self.hbox.children = (*self.hbox.children, container)

    def trunc(self, last):
        self.hbox.children = self.hbox.children[0:last]
