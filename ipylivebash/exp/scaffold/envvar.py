import os
from .scaffoldvar import ScaffoldVar
from .inputoutputmixin import InputOutputOptions


class EnvVar(ScaffoldVar):
    """
    Wrapper for environment variable
    """

    def __init__(self, key, defaults=""):
        self.key = key
        self.defaults = defaults

    def write(self, value=None, options: InputOutputOptions = None):
        validaed_value = self.validate(value, self.defaults)
        os.environ[self.key] = validaed_value
        if options is not None and options.print_line is not None:
            options.print_line(f"Set {self.key}={value}\n")

    def read(self, options: InputOutputOptions = None):
        return os.getenv(self.key)
