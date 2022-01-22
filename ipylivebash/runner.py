from IPython.display import display
import ipywidgets as widgets
import subprocess
import argparse
import sys
import time
import threading
from .logview import LogView
from .logfile import LogFile


def run_script(script):
    """
    Run script via Python API.
    It is an internal testing API.
    """
    runner = Runner("")
    runner.run(script)


class RunScriptProxy:
    def __init__(self):
        self.mutex = threading.Lock()
        self.is_finished = False
        self.error = None
        self.messages = []

    def acquire(self):
        self.mutex.acquire()

    def release(self):
        self.mutex.release()


def execute_script_in_thread(script):
    def worker(proxy, script):
        try:
            process = subprocess.Popen(script,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       shell=True,
                                       universal_newlines=True,
                                       executable='/bin/bash')
            for line in process.stdout:
                proxy.acquire()
                proxy.messages.append(line)
                proxy.release()
        except Exception as e:
            proxy.acquire()
            proxy.error = e
            proxy.release()

        proxy.acquire()
        if process.wait() != 0:
            proxy.error = Exception("Failed!")

        proxy.is_finished = True
        proxy.release()

    proxy = RunScriptProxy()
    thread = threading.Thread(target=worker, args=(proxy, script))
    thread.start()
    return proxy


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
        if self.args.output_file is not None:
            self.log_file = LogFile(
                pattern=self.args.output_file,
                use_timestamp=self.args.use_timestamp
            )
        self.log_view.height = self.args.height
        self.container = widgets.VBox(
            [self.log_view]
        )
        self.grid_box = widgets.GridBox(
            children=[self.container],
            layout=widgets.Layout(
                width="100%",
                grid_template_rows='auto',
                grid_template_columns='100%'
            )
        )

    def run(self, script):
        display(self.grid_box)
        funcs = [
            lambda next: self.execute_confirmation(next),
            lambda next: self.execute_notification(next),
            lambda next: self.execute_logger(next),
            lambda next: self.execute_script(script, next)
        ]
        run_chain(funcs)

    def execute_confirmation(self, next):
        if self.args.ask_confirm is not True:
            next()
            return

        confirm_button = widgets.Button(description="Confirm")
        cancel_button = widgets.Button(description="Cancel")
        output = widgets.Output()
        hbox = widgets.HBox([confirm_button, cancel_button])

        def confirm(_):
            hbox.layout.display = 'none'
            output.layout.display = 'none'
            next()

        def cancel(_):
            hbox.layout.display = 'none'
            with output:
                print("")
                print("Canceled")

        confirm_button.on_click(confirm)
        cancel_button.on_click(cancel)
        self.container.children = [output, hbox] + \
            list(self.container.children)

        with output:
            print("Are you sure you want to run this script?")

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
        self.is_executed = True
        self.log_view.running = True

        try:
            proxy = execute_script_in_thread(script)
            while True:
                time.sleep(0.1)
                proxy.acquire()
                messages = proxy.messages
                is_finished = proxy.is_finished
                error = proxy.error
                proxy.messages = []
                proxy.release()

                if len(messages) > 0:
                    for message in messages:
                        self.write_message(message)
                    self.flush()

                if is_finished or error is not None:
                    break
        except Exception as e:
            error = e

        self.log_view.flush()
        self.log_view.running = False

        if error is not None:
            raise error

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
