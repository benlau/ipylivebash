"""
LogView Widget
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Any, Int, Bool
from ._frontend import module_name, module_version
from .debounce import debounce

UNKNOWN = "unknown"
STATUS_TEXT_LINE_LIMIT = 5


class LogView(DOMWidget):
    """LogView
    """
    _model_name = Unicode('LogViewModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('LogView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    messages = Any([]).tag(sync=True)
    status_header = Unicode('').tag(sync=True)
    status = Any([]).tag(sync=True)
    height = Int(0).tag(sync=True)

    notification_permission_request = Bool(False).tag(sync=True)
    notification_permission = Unicode(UNKNOWN).tag(sync=True)

    notification_message = Unicode('').tag(sync=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submitted_count = 0
        self.messages_buffer = []
        self.status_buffer = []

    def write_message(self, line):
        self.messages_buffer.append(line)
        self.submit()

    def write_status(self, status):
        self.status_buffer.append(status)
        if len(self.status_buffer) > STATUS_TEXT_LINE_LIMIT:
            self.status_buffer = self.status_buffer[1:]
        self.submit()

    def flush(self):
        if len(self.status_buffer) > 0:
            self.status = self.status_buffer.copy()
        if len(self.messages_buffer) == 0:
            return
        messages = [self.submitted_count] + self.messages_buffer
        self.submitted_count = self.submitted_count + 1
        self.messages_buffer = []
        self.messages = messages

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
