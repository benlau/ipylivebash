from ..patchers.assign import PatchAssignment
from .scaffoldvar import ScaffoldVar


class EnvFileVar(ScaffoldVar):
    def __init__(self, filename, key, defaults=None):
        self.filename = filename
        self.key = key
        self.patcher = PatchAssignment()
        self.defaults = defaults

    def write(self, value, options=None):
        content = self._read_file_content()
        replaced, _ = self.patcher(
            content if content is not None else "", self.key, value
        )

        file = open(self.filename, "w")
        file.write(replaced)
        file.close()

        if options is not None and options.print_line is not None:
            options.print_line(f"Set {self.key}={value} to {self.filename}\n")

    def read(self, options=None):
        content = self._read_file_content()
        if content is None:
            return None

        _, value = self.patcher(content, self.key)
        return value

    def _read_file_content(self):
        try:
            file = open(self.filename, "r")
            content = file.read()
            file.close()
            self.content = content
        except FileNotFoundError:
            return None
        return content
