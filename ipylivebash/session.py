from enum import Enum
from .run_task import RunTask

SHELL = "/bin/bash"


class SessionState(Enum):
    NotStarted = "NotStarted"
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

    def run(self, print=print, flush=None):
        self.task = RunTask()
        self.task.script = self.script
        return self.task(print=print, flush=flush)

    def kill(self):
        self.task.kill()
