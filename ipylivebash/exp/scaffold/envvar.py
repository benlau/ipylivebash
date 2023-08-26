import os


class EnvVar:
    """
    Wrapper for environment variable
    """

    def __init__(self, name):
        self.name = name

    def __call__(self, value, output):
        os.environ[self.name] = value
        output(f"Set {self.name}={value}")
