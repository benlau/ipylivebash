from IPython.display import display
import ipywidgets as widgets
import subprocess
import argparse
import sys
import time
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
        self.bottom_text = []
        self.bottom_text_max_line_count = 5
        self.is_executed = False
        if self.args.output_file is not None:
            self.log_file = LogFile(
                pattern=self.args.output_file,
                use_timestamp=self.args.use_timestamp
            )
        self.log_view.height = self.args.height

    def run(self, script):
        funcs = [
            lambda next: self.confirm_run(next),
            lambda next: self.notify(next),
            lambda next: self.execute(script, next)
        ]
        display(self.log_view)
        run_chain(funcs)

    def confirm_run(self, next):
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

        display(output)
        confirm_button.on_click(confirm)
        cancel_button.on_click(cancel)

        with output:
            print("Are you sure you want to run this script?")
        display(hbox)

    def write_line(self, line):
        self.line_printed = self.line_printed + 1
        if self.args.output_file is not None:
            self.log_file.write_line(line)

        if self.args.keep_cell_output is True:
            sys.stdout.write(line)
            return

        if (self.line_printed >= self.args.line_limit and
                self.args.line_limit > 0):
            if self.log_view.divider_text == "":
                self.log_view.divider_text = "=== Output exceed the max line limitation. Only the latest output will be shown ==="  # noqa
            if len(self.bottom_text) >= self.bottom_text_max_line_count:
                self.bottom_text = self.bottom_text[1:]
            self.bottom_text.append(line)
            self.log_view.bottom_text = self.bottom_text.copy()
        else:
            self.log_view.write_line(line)

    def execute(self, script, next):
        if self.is_executed:
            return
        self.is_executed = True

        if self.args.output_file is not None:
            self.log_file.open()

        process = subprocess.Popen(script,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   shell=True,
                                   universal_newlines=True,
                                   executable='/bin/bash')
        for line in process.stdout:
            self.write_line(line)

        time.sleep(0.1)
        self.log_view.flush()

        if process.wait() != 0:
            raise Exception("Failed!")

        next()

    def notify(self, next):
        if self.args.send_notification is False:
            next()
            return

        def callback(permission):
            if permission != "granted":
                self.log_view.write_line(
                    f"Request notification permission failed: {permission}")
                return
            next()
            self.log_view.notification_message = "The script is finished"

        self.log_view.request_notification_permission(callback)
