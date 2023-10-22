import os
from .scaffoldvar import ScaffoldVar
from .context import Context
from .decorators import preset_format


class EnvVar(ScaffoldVar):
    """
    Wrapper for environment variable
    """

    @preset_format
    def __init__(self, key, defaults=""):
        self.key = key
        self.defaults = defaults

    def get_id(self):
        return f"Env:{self.key}"

    def write(self, value=None, context: Context = None):
        validaed_value = self.validate(value, self.defaults)
        os.environ[self.key] = validaed_value
        if context is not None and context.print_line is not None:
            context.print_line(f"Set {self.key}={value}\n")

    def read(self, context: Context = None):
        return os.getenv(self.key)
