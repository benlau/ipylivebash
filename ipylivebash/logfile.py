import re
import os
import datetime


class LogFile:
    def __init__(self, pattern="output.log", use_timestamp=False):
        self.pattern = pattern
        self.use_timestamp = use_timestamp

    def open(self):
        suffix = None
        filename = LogFile.gen_filename(
            self.pattern, suffix=suffix, use_timestamp=self.use_timestamp
        )
        suffix = 0
        while True:
            if not os.path.isfile(filename):
                break

            suffix = suffix + 1
            filename = LogFile.gen_filename(
                self.pattern, suffix=suffix, use_timestamp=self.use_timestamp
            )

        self.fd = open(filename, "wt")
        return

    def write_message(self, line):
        self.fd.write(line)

    def close(self):
        self.fd.close()

    def flush(self):
        if self.fd is not None:
            self.fd.flush()

    @classmethod
    def gen_filename(cls, pattern, suffix=None, use_timestamp=False):
        if use_timestamp is True:
            now = datetime.datetime.now()
            suffix = now.strftime("%Y%m%d-%H%M%S")

        if suffix is None:
            return pattern

        match = re.search("^(.*)\\.(.*)$", pattern)
        if match is None:
            return f"{pattern}-{suffix}"

        return f"{match.group(1)}-{suffix}.{match.group(2)}"
