import os
from .scaffoldvar import ScaffoldVar


class EnvVar(ScaffoldVar):
    """
    Wrapper for environment variable
    """

    def __init__(self, variable_name, default_variable_value=""):
        self.variable_name = variable_name
        self.default_variable_value = default_variable_value

    def write(self, value):
        os.environ[self.variable_name] = value

    def write_message(self, value):
        return f"Set {self.variable_name}={value}"

    def read(self):
        return os.getenv(self.variable_name, self.default_variable_value)
