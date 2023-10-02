import os
from .scaffoldvar import ScaffoldVar
from .inputoutputmixin import IOOptions
from .decorators import preset_format


class EnvVar(ScaffoldVar):
    """
    Wrapper for environment variable
    """

    @preset_format
    def __init__(self, key, defaults=""):
        self.key = key
        self.defaults = defaults

    def write(self, value=None, options: IOOptions = None):
        validaed_value = self.validate(value, self.defaults)
        os.environ[self.key] = validaed_value
        if options is not None and options.print_line is not None:
            options.print_line(f"Set {self.key}={value}\n")

    def read(self, options: IOOptions = None):
        return os.getenv(self.key)
