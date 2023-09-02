from ..patchers.assign import PatchAssignment
from .scaffoldvar import ScaffoldVar


class EnvFileVar(ScaffoldVar):
    def __init__(self, file_name, variable_name):
        self.file_name = file_name
        self.variable_name = variable_name
        self.patcher = PatchAssignment()

    def write(self, variable_value):
        content = self._read_file_content()
        replaced, _ = self.patcher(content, self.variable_name, variable_value)

        file = open(self.file_name, "w")
        file.write(replaced)
        file.close()

    def write_message(self, value):
        return f"Set {self.variable_name}={value} to {self.file_name}"

    def read(self, default_value=""):
        content = self._read_file_content()

        _, value = self.patcher(content, self.variable_name)
        if value is None:
            return default_value
        return value

    def _read_file_content(self):
        file = open(self.file_name, "r")
        content = file.read()
        file.close()
        self.content = content
        return content
