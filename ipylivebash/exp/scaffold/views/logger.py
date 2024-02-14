from ipylivebash.exp.scaffold.doublebufferoutput import DoubleBufferOutput
from ipywidgets import widgets
from IPython.display import display
import uuid


# Logger is a view class that is used to log messages
class Logger:
    def __init__(self, line_limit=100):
        self.id = uuid.uuid4()
        self.line_limit = line_limit
        self.line_count = 0
        self.content = ""
        self._create_widget()

    def _create_widget(self):
        html = widgets.HTML(value=self.render())
        vbox = widgets.VBox([html])
        self.widget = vbox
        self.html = html

    def append_stdout(self, message):
        self.content = self.content + "\n" + message
        self.refresh()

    def clear_output(self):
        self.content = ""
        self.refresh()

    def refresh(self):
        self.html.value = self.render()

    def show(self):
        display(self.widget)

    def render(self):
        normalized_id = str(self.id).replace("-", "")
        container_class_name = f"scaffold_container_{normalized_id}"
        copy_button_class_name = f"scaffold_copy_button_{normalized_id}"

        js = f"""
            var range = document.createRange();
            var elm = document.getElementById('{normalized_id}');
            console.log(elm);
            range.selectNode(elm);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand("copy");
            window.getSelection().removeAllRanges();
        """.replace(
            '"', "&quot;"
        )
        # widgets.html can't insert script block, so we use escaped js
        return f"""
<div class="{container_class_name}">
    <style>
    .{container_class_name} {{
        border: 1px solid #bfbfbf; padding: 4px 4px;min-height: 80px;
    }}
    .{copy_button_class_name}:hover {{
        opacity: 0.5;
    }}
    .{copy_button_class_name}:active {{
        opacity: 0.8;
    }}
    .{copy_button_class_name} {{
        position: absolute;
        right: 0px;
        top: 0px;
        border: 1px solid #bfbfbf;
        display: block;
        border: 1px solid #bfbfbf; 
        padding: 2px 4px;
        user-select: none;
    }};
    </style>
    <pre id={normalized_id}>{self.content}</pre>
    <div class="{copy_button_class_name}" onclick="{js}">Copy</div>
</div>
"""
