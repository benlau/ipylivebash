import ipywidgets as widgets


class DoubleBufferOutput:
    """
    An alternative to ipywidgets.Output that uses a double buffer to avoid unable to clear output bug.

    https://stackoverflow.com/questions/58380894/ipywidgets-clear-output-does-not-work-the-second-time-its-used
    """

    def __init__(self):
        self.active = 0
        self.outputs = list(map(lambda i: widgets.Output(), range(2)))
        self.vbox = widgets.VBox(self.outputs)
        self.refresh()

    def refresh(self):
        self.outputs[self.active].layout.visibility = "visible"
        self.outputs[1 - self.active].layout.visibility = "hidden"

    @property
    def append_stdout(self):
        return self.outputs[self.active].append_stdout

    def clear_output(self):
        self.outputs[self.active].clear_output()
        self.active = 1 - self.active
        self.refresh()
