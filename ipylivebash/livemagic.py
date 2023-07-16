from IPython.display import display
import argparse
from .sessionmanager import SessionManager


class LiveMagic:
    def __init__(self, session_manager=SessionManager.get_instance()):
        self.session_manager = session_manager
        self.session = None

    def parse(self, args):
        parser = argparse.ArgumentParser(prog="livebash", add_help=False)
        parser.add_argument("-h", "--help", action="store_true", dest="print_help")
        parser.add_argument(
            "-ps", "--print-sessions", action="store_true", dest="print_sessions"
        )
        parser.add_argument(
            "--save", dest="output_file", type=str, help="Save output to a file"
        )
        parser.add_argument(
            "--save-timestamp",
            action="store_true",
            dest="use_timestamp",
            help="Add timestamp to the output file name",
        )
        parser.add_argument(
            "--line-limit",
            dest="line_limit",
            default=0,
            type=int,
            help="Restrict the no. of lines to be shown",
        )
        parser.add_argument(
            "--height",
            dest="height",
            default=10,
            type=int,
            help="Set the height of the output cell (no. of line)",
        )
        parser.add_argument(
            "--ask-confirm",
            action="store_true",
            dest="ask_confirm",
            help="Ask for confirmation before execution",
        )
        parser.add_argument(
            "--notify",
            action="store_true",
            dest="send_notification",
            help="Send a notification when the script finished",
        )
        self.args = parser.parse_args(args)
        self.parser = parser

    def run(self, script):
        session = self.session_manager.create_session()
        session.script = script
        self.session_manager.run_session_with_view(session, self.args)
