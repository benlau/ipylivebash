from IPython.display import display
import ipywidgets as widgets
import subprocess
import argparse
import sys
import time
import threading
import json
from .logview import LogView
from .logfile import LogFile


def run_script(script):
    """
    Run script via Python API.
    It is an internal testing API.
    """
    runner = Runner("")
    runner.run(script)


def run_chain(funcs):
    if len(funcs) == 0:
        return
    remaining = funcs[1:]
    func = funcs[0]

    def next():
        run_chain(remaining)

    func(next)


class Runner:
    def __init__(self, args):
        parser = argparse.ArgumentParser(prog="livebash", add_help=False)
        parser.add_argument('-h', '--help',
                            action='store_true', dest='print_help')
        parser.add_argument('--save',
                            dest='output_file', type=str, help="Save output to a file")
        parser.add_argument('--save-timestamp',
                            action='store_true', dest='use_timestamp',
                            help="Add timestamp to the output file name")
        parser.add_argument('--line-limit',
                            dest='line_limit', default=0, type=int,
                            help="Restrict the no. of lines to be shown")
        parser.add_argument('--height',
                            dest='height', default=0, type=int,
                            help="Set the height of the output cell (no. of line)")
        parser.add_argument('--ask-confirm',
                            action='store_true', dest='ask_confirm',
                            help="Ask for confirmation before execution")
        parser.add_argument('--notify',
                            action='store_true', dest='send_notification',
                            help="Send a notification when the script finished")
        parser.add_argument('--keep-cell-output',
                            action='store_true', dest='keep_cell_output',
                            help="Keep the cell output")
        self.args = parser.parse_args(args)
        self.parser = parser
        self.log_view = LogView()
        self.line_printed = 0
        self.is_executed = False
        
        self.process = None
        self.process_finish_messages = [""]
        
        if self.args.output_file is not None:
            self.log_file = LogFile(
                pattern=self.args.output_file,
                use_timestamp=self.args.use_timestamp
            )
        self.log_view.height = self.args.height
        self.log_view.observe(self.on_response, names='response')

    def run(self, script):
        self.script = script
        display(self.log_view)
        funcs = [
            lambda next: self.execute_confirmation(next),
            lambda _: self.run_without_confirmation(),
        ]
        run_chain(funcs)

    def run_without_confirmation(self):
        funcs = [
            lambda next: self.execute_notification(next),
            lambda next: self.execute_logger(next),
            lambda next: self.execute_script(self.script, next)
        ]
        run_chain(funcs)

    def execute_confirmation(self, next):
        if self.args.ask_confirm is not True:
            next()
            return

        self.log_view.confirmation_required = True

    def flush(self):
        self.log_view.flush()
        if self.args.output_file is not None:
            self.log_file.flush()

    def write_message(self, line):
        self.line_printed = self.line_printed + 1
        if self.args.output_file is not None:
            self.log_file.write_message(line)

        if self.args.keep_cell_output is True:
            sys.stdout.write(line)
            return

        if (self.line_printed >= self.args.line_limit and
                self.args.line_limit > 0):
            if self.log_view.status_header == "":
                self.log_view.status_header = "=== Output exceed the line limitation. Only the latest output will be shown ==="  # noqa
            self.log_view.write_status(line)
        else:
            self.log_view.write_message(line)

    def execute_script(self, script, next):
        if self.is_executed:
            return
        self.log_view.clear()
        self.is_executed = True
        self.log_view.running = True
        self.line_printed = 0
        self.process_finish_messages = []

        def worker():
            pending_messages = []
            last_flush_time = time.time()
            try:
                # Pause a while to make sure the frontend 
                # could receive the property changes
                time.sleep(0.1)
                process = subprocess.Popen(script,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        shell=True,
                                        universal_newlines=True,
                                        executable='/bin/bash')
                self.process = process
                for line in process.stdout:
                    pending_messages.append(line)
                    current_time = time.time()
                    if current_time - last_flush_time > 0.1:
                        if len(pending_messages) > 0:
                            for message in pending_messages:
                                self.write_message(message)
                            self.flush()
                        pending_messages = []
                        last_flush_time = current_time
            except Exception as e:
                self.process_finish_messages.append(str(e))

            for message in pending_messages:
                self.write_message(message)

            for message in self.process_finish_messages:
                self.write_message(message)

            self.write_message(f"Process finished with exit code {process.poll()}")
            self.flush()

            self.is_executed = False
            self.log_view.running = False

        thread = threading.Thread(target=worker, args=())
        thread.start()
        next()

    def execute_notification(self, next):
        if self.args.send_notification is False:
            next()
            return

        def callback(permission):
            if permission != "granted":
                self.log_view.write_message(
                    f"Request notification permission failed: {permission}")
                return
            next()
            self.log_view.notification_message = "The script is finished"

        self.log_view.request_notification_permission(callback)

    def execute_logger(self, next):
        if self.args.output_file is not None:
            self.log_file.open()
            next()
            self.log_file.close()
        else:
            next()

    def on_response(self, change):
        response = json.loads(change.new)
        content = json.loads(response['content'])
        if content['type'] == 'requestToStop':
            self.process_finish_messages.append("Force terminated")
            self.process.terminate()
        elif content['type'] == 'confirmToRun':
            self.run_without_confirmation()
