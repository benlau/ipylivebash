from .logfile import LogFile
from .session import Session, SessionState
import asyncio
from .logview import LogView
from .utils import run_chain, left_pad
from IPython.display import display
import time
import json
from tabulate import tabulate
from IPython import get_ipython
from enum import Enum


instance = None


class EventType(Enum):
    RequestToKill = "RequestToKill"
    ConfirmedToRun = "ConfirmedToRun"
    CancelledToRun = "CancelledToRun"


async def run_script(script):
    """
    Run script via Python API without UI.
    """

    def output(message):
        print(message.strip())

    manager = SessionManager.get_instance()
    session = manager.create_session()
    session.script = script
    return await manager.run_session(session, output=output)


class SessionManager:
    def __init__(self, max_completed_session=10):
        self.sessions = []
        self.next_id = 1
        self.max_completed_session = max_completed_session
        self.views = []
        self.notification_id = 1
        self.current_cell_id = None

    def _on_pre_run_cell(self, info):
        self.current_cell_id = info.cell_id

    def start(self):
        ip = get_ipython()
        ip.events.register("pre_run_cell", self._on_pre_run_cell)

    def refresh_sessions(self):
        stored_finished_session = 0

        def predicate(session):
            nonlocal stored_finished_session
            if session.is_finished:
                if stored_finished_session < self.max_completed_session:
                    stored_finished_session = stored_finished_session + 1
                else:
                    return False
            return True

        self.sessions.reverse()
        self.sessions = list(filter(predicate, self.sessions))
        self.sessions.reverse()

        sessions = [
            {
                "id": session.id,
                "state": session.state.value,
            }
            for session in self.sessions
        ]

        self.set_all_view_property("sessions", sessions)

    def print_sessions(self):
        headers = ["Session ID", "State"]
        rows = [[session.id, session.state.value] for session in self.sessions]
        print(tabulate(rows, headers=headers))

    def create_session(self):
        session = Session()
        session.id = f"instance{left_pad(str(self.next_id), 4, '0')}"
        session.cell_id = self.current_cell_id
        self.current_cell_id = None
        self.next_id = self.next_id + 1
        self.sessions.append(session)
        return session

    def create_view(self, session):
        view = LogView(session_id=session.id, cell_id=session.cell_id)
        for v in self.views:
            if v.cell_id == view.cell_id:
                self.views.remove(v)
        self.views.append(view)
        return view

    async def run_session(self, session, output=print):
        session.args = {}
        session.state = SessionState.Running
        self.refresh_sessions()

        try:
            exit_code = await session.run(output=output)
            session.state = SessionState.Completed
            session.exit_code = exit_code
        except asyncio.CancelledError:
            self.kill(session.id)
            print("Force terminated")
            session.state = SessionState.ForceTerminated

        self.refresh_sessions()

    def run_session_with_view(self, session, args):
        session.args = args

        view = self.create_view(session)
        self.set_view_property(session, "height", args.height)
        self.set_view_property(session, "script", session.script)
        self.refresh_sessions()

        if args.ask_confirm is True:
            self.set_view_property(session, "confirmation_required", True)

        def on_response(change):
            self.on_response(view.session_id, change)

        view.observe(on_response, names="response")
        display(view)

        funcs = [
            lambda next: self.execute_confirmation(session, next),
            lambda next: self.execute_logger(session, next),
            lambda next: self.execute_notification(session, next),
            lambda next: self.execute_process(session, next),
        ]
        run_chain(funcs)

    def execute_confirmation(self, session, next):
        if session.args.ask_confirm is not True:
            next()
            return

        session.next = next

    def execute_logger(self, session, next):
        if session.args.output_file is not None:
            try:
                log_file = LogFile(
                    pattern=session.args.output_file,
                    use_timestamp=session.args.use_timestamp,
                )
                log_file.open()
                session.log_file = log_file
            except OSError as e:
                time.sleep(0.1)
                self.write_message(session.id, str(e))
                self.flush(session.id)
                return
        next()

    def execute_notification(self, session, next):
        if session.args.send_notification is not True:
            next()
            return

        # Any one of a view works
        view = self.views[-1]

        def callback(permission):
            if permission != "granted":
                view.write_message(
                    f"Request notification permission failed: {permission}"
                )
                view.flush()
                return
            next()

        view.request_notification_permission(callback)

    def execute_process(self, session, next):
        session_id = session.id

        self.set_view_property(session, "running", True)
        session.state = SessionState.Running
        self.refresh_sessions()

        def output(message):
            self.write_message(session_id, message)

        def flush():
            self.flush(session_id)

        future = session.run(output=output, flush=flush)

        def on_finish():
            self.on_session_finished(session_id, future.result())
            next()

        future.add_done_callback(lambda _: on_finish())

    def write_message(self, session_id, message):
        session = self.find_session(session_id)
        if session is None:
            return

        session.line_printed = session.line_printed + 1
        args = session.args

        if session.log_file is not None:
            session.log_file.write_message(message)

        for view in self.views:
            if view.session_id == session_id:
                if session.line_printed >= args.line_limit and args.line_limit > 0:
                    if view.status_header == "":
                        view.status_header = "=== Output exceed the line limitation. Only the latest output will be shown ==="  # noqa
                    view.write_status(message)
                else:
                    view.write_message(message)

    def flush(self, session_id):
        session = self.find_session(session_id)

        if session.log_file is not None:
            session.log_file.flush()

        for view in self.views:
            if view.session_id == session_id:
                view.flush()

    def set_view_property(self, session, key, value):
        for view in self.views:
            if view.cell_id == session.cell_id:
                setattr(view, key, value)

    def set_all_view_property(self, key, value):
        for view in self.views:
            setattr(view, key, value)

    def on_session_finished(self, session_id, exit_code):
        session = self.find_session(session_id)
        if session is None:
            return

        session.exit_code = exit_code

        pending_messages = []

        for message in session.process_finish_messages:
            pending_messages.append(message)

        if len(session.process_finish_messages) == 0:
            pending_messages.append(
                f"Process finished with exit code {session.exit_code}"
            )

        for message in pending_messages:
            self.write_message(session_id, message)
        self.flush(session_id)
        self.set_view_property(session, "running", False)

        if session.log_file is not None:
            session.log_file.close()

        if session.args.send_notification is True:
            self.send_notification(session.id, "The script is finished")
        if session.state is not SessionState.ForceTerminated:
            session.state = SessionState.Completed

        self.refresh_sessions()

    def send_notification(self, session_id, message):
        payload = {"id": self.notification_id, "message": message}
        self.notification_id = self.notification_id + 1
        for view in self.views:
            if view.session_id == session_id:
                setattr(view, "notification_message", payload)
                break

    def find_session(self, id):
        for session in self.sessions:
            if session.id == id:
                return session

    def on_response(self, session_id, change):
        try:
            response = json.loads(change.new)
            content = json.loads(response["content"])
            if content["type"] == EventType.RequestToKill.value:
                target_session_id = content["target_session_id"]
                session = self.find_session(target_session_id)
                if session is not None:
                    session.process_finish_messages.append("Force terminated")
                    self.kill(target_session_id)
            elif content["type"] == EventType.ConfirmedToRun.value:
                session = self.find_session(session_id)
                next = session.next
                session.next = None
                next()
            elif content["type"] == EventType.CancelledToRun.value:
                session = self.find_session(session_id)
                session.state = SessionState.Cancelled
                self.refresh_sessions()

        except Exception as e:
            print(e)

    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = SessionManager()
        return instance

    def kill(self, session_id):
        session = self.find_session(session_id)
        if session is None:
            return

        session.kill()
        session.state = SessionState.ForceTerminated
