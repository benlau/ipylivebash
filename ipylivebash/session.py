from enum import Enum
from .runtask import RunTask

SHELL = "/bin/bash"


class SessionState(Enum):
    NotStarted = "NotStarted"
    Cancelled = "Cancelled"
    Running = "Running"
    Completed = "Completed"
    ForceTerminated = "ForceTerminated"


class Session:
    def __init__(self):
        self.id = None
        self.name = "Unnamed Session"
        self.log_file = None
        self.script = ""
        self.state = SessionState.NotStarted
        self.task = None
        self.line_printed = 0
        self.args = None
        self.process_finish_messages = []
        self.exit_code = None
        self.cell_id = None

        # next function to be involved
        self.next = None

    def run(self, output=print, flush=None):
        self.task = RunTask()
        self.task.script = self.script
        return self.task(output=output, flush=flush)

    def kill(self):
        self.task.kill()

    @property
    def is_finished(self):
        return (
            self.state == SessionState.Completed
            or self.state == SessionState.ForceTerminated
            or self.state == SessionState.Cancelled
        )
