from ..patchers.assign import PatchAssignment
from .scaffoldvar import ScaffoldVar


class EnvFileVar(ScaffoldVar):
    def __init__(self, file_name, variable_name, default_variable_value=None):
        self.file_name = file_name
        self.variable_name = variable_name
        self.patcher = PatchAssignment()
        self.default_value = default_variable_value

    def write(self, variable_value):
        content = self._read_file_content()
        replaced, _ = self.patcher(content, self.variable_name, variable_value)

        file = open(self.file_name, "w")
        file.write(replaced)
        file.close()

    def write_message(self, value):
        return f"Set {self.variable_name}={value} to {self.file_name}"

    def read(self):
        content = self._read_file_content()
        if content is None:
            return self.default_value

        _, value = self.patcher(content, self.variable_name)
        if value is None:
            return self.default_variable_value
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
