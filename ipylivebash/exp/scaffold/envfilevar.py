from ..patchers.assign import PatchAssignment
from .scaffoldvar import ScaffoldVar


class EnvFileVar(ScaffoldVar):
    def __init__(self, file_name, key, defaults=None):
        self.file_name = file_name
        self.key = key
        self.patcher = PatchAssignment()
        self.defaults = defaults

    def write(self, value):
        content = self._read_file_content()
        replaced, _ = self.patcher(content, self.key, value)

        file = open(self.file_name, "w")
        file.write(replaced)
        file.close()

    def write_message(self, value):
        return f"Set {self.key}={value} to {self.file_name}"

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
            file = open(self.file_name, "r")
            content = file.read()
            file.close()
            self.content = content
        except FileNotFoundError:
            return None
        return content
