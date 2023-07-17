"""
LogView Widget
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Any, Int, Bool
import json
from ._frontend import module_name, module_version
import string
import random

UNKNOWN = "unknown"
STATUS_TEXT_LINE_LIMIT = 5


class LogView(DOMWidget):
    """LogView"""

    _model_name = Unicode("LogViewModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("LogView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    session_id = Unicode("").tag(sync=True)

    cell_id = Unicode("").tag(sync=False)

    # Latest messages
    messages = Any([]).tag(sync=True)

    # The script for the current session
    script = Unicode("").tag(sync=True)

    status_header = Unicode("").tag(sync=True)
    status = Any([]).tag(sync=True)
    height = Int(0).tag(sync=True)
    running = Bool(False).tag(sync=True)
    confirmation_required = Bool(False).tag(sync=True)

    notification_permission_request = Bool(False).tag(sync=True)
    notification_permission = Unicode(UNKNOWN).tag(sync=True)

    notification_message = Any({}).tag(sync=True)

    response = Unicode("").tag(sync=True)
    action = Unicode("").tag(sync=True)

    sessions = Any([]).tag(sync=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submitted_count = 0
        self.messages_buffer = []
        self.status_buffer = []
        self.instance_id = "".join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8
            )
        )

    def __repr__(self):
        return f""

    def write_message(self, line):
        self.messages_buffer.append(line)

    def write_status(self, status):
        self.status_buffer.append(status)
        if len(self.status_buffer) > STATUS_TEXT_LINE_LIMIT:
            self.status_buffer = self.status_buffer[1:]

    def flush(self):
        if len(self.status_buffer) > 0:
            self.status = self.status_buffer.copy()
        if len(self.messages_buffer) == 0:
            return
        messages = [self.submitted_count] + self.messages_buffer
        self.submitted_count = self.submitted_count + 1
        self.messages_buffer = []
        self.messages = messages

    def clear(self):
        self.messages = []
        self.status = []
        self.status_header = ""
        self.submitted_count = 0

    def request_notification_permission(self, callback):
        if self.notification_permission != UNKNOWN:
            callback(self.notification_permission)

        def getvalue(change):
            self.unobserve(getvalue, "notification_permission")
            callback(change["new"])

        self.observe(getvalue, "notification_permission")
        self.notification_permission_request = True
        self.notification_permission_request = False

    def send_action(self, content: str):
        self.action = ""
        self.action = json.dumps(
            {"id": self.instance_id + f":{self.submitted_count}", "content": content}
        )
        self.submitted_count = self.submitted_count + 1
