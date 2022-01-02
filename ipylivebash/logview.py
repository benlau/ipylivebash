"""
LogView Widget
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Any, Int, Bool
from ._frontend import module_name, module_version
from .debounce import debounce

UNKNOWN = "unknown"


class LogView(DOMWidget):
    """LogView
    """
    _model_name = Unicode('LogViewModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('LogView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    lines = Any([]).tag(sync=True)
    divider_text = Unicode('').tag(sync=True)
    bottom_text = Any([]).tag(sync=True)
    height = Int(0).tag(sync=True)

    notification_permission_request = Bool(False).tag(sync=True)
    notification_permission = Unicode(UNKNOWN).tag(sync=True)

    notification_message = Unicode('').tag(sync=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submitted_count = 0
        self.lines_buffer = []

    def write_line(self, line):
        self.lines_buffer.append(line)
        self.submit()

    def flush(self):
        if len(self.lines_buffer) == 0:
            return
        lines = [self.submitted_count] + self.lines_buffer
        self.submitted_count = self.submitted_count + 1
        self.lines_buffer = []
        self.lines = lines

    @debounce(0.1)
    def submit(self):
        self.flush()

    def request_notification_permission(self, callback):
        if self.notification_permission != UNKNOWN:
            callback(self.notification_permission)

        def getvalue(change):
            self.unobserve(getvalue, "notification_permission")
            callback(change["new"])

        self.observe(getvalue, "notification_permission")
        self.notification_permission_request = True
        self.notification_permission_request = False
