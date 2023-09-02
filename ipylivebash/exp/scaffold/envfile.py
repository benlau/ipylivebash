from ..patchers.assign import PatchAssignment


class EnvFile:
    def __init__(self, file_name, variable_name):
        self.file_name = file_name
        self.variable_name = variable_name
        self.patch_assignment = PatchAssignment()
        self.content = None

    def __call__(self, value, output):
        self._read()
        replaced, _ = self.patch_assignment(self.content, self.variable_name, value)

        file = open(self.file_name, "w")
        file.write(replaced)
        file.close()

        self.content = replaced
        output(f"Set {self.variable_name}={value}")

    def __str__(self):
        self._read()

        _, value = self.patch_assignment(self.content, self.variable_name)
        return value

    def _read(self):
        if self.content is not None:
            return self.content

        file = open(self.file_name, "r")
        content = file.read()
        file.close()
        self.content = content
        return content
