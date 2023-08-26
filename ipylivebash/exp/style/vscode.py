import ipywidgets as widgets
from IPython.display import display


def apply_style():
    """
    Set the ipywidget background to transparent for bot of dark and light theme
    """

    style = """\
<style>
.cell-output-ipywidget-background {
   background-color: transparent !important;
}
.jp-OutputArea-output {
   background-color: transparent;
}      
</style>
    """
    display(widgets.HTML(style))
