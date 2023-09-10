from ..patchers.assign import PatchAssignment
from .scaffoldvar import ScaffoldVar


class EnvFileVar(ScaffoldVar):
    def __init__(self, filename, key, defaults=None):
        self.filename = filename
        self.key = key
        self.patcher = PatchAssignment()
        self.defaults = defaults

    def write(self, value):
        content = self._read_file_content()
        replaced, _ = self.patcher(
            content if content is not None else "", self.key, value
        )

        file = open(self.filename, "w")
        file.write(replaced)
        file.close()

    def write_message(self, value):
        return f"Set {self.key}={value} to {self.filename}\n"

    def read(self):
        content = self._read_file_content()
        if content is None:
            return self.defaults

        _, value = self.patcher(content, self.key)
        if value is None:
            return self.defaults
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
