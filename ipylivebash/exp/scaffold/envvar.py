import os
from .scaffoldvar import ScaffoldVar


class EnvVar(ScaffoldVar):
    """
    Wrapper for environment variable
    """

    def __init__(self, key, defaults=""):
        self.key = key
        self.defaults = defaults

    def write(self, value=None):
        validaed_value = self.valiate(value, self.defaults)
        os.environ[self.key] = validaed_value

    def write_message(self, value):
        return f"Set {self.key}={value}\n"

    def read(self):
        return os.getenv(self.key)
