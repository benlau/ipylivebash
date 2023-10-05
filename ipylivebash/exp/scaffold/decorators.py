from ipylivebash.sessionmanager import run_script  # noqa
from .utils import inspect_arg_name
from .format import Format


def _setup_iot(input, output, title):
    if output is None and not isinstance(input, list):
        output = input

    return (input, output, title)


def preset_iot(func):
    """
    A decorator that preset the input, output, title arguments
    """

    def inner(input=None, output=None, title=None, *args, **kwargs):
        if title is None:
            if input is not None:
                title = inspect_arg_name(0, "input")
            elif output is not None:
                title = inspect_arg_name(1, "output")
        (input, output, title) = _setup_iot(input, output, title)
        return func(input, output, title, *args, **kwargs)

    return inner


def preset_iot_class_method(func):
    """
    A decorator that preset the input, output, title arguments
    """

    def inner(self, input=None, output=None, title=None, *args, **kwargs):
        if title is None:
            if input is not None:
                title = inspect_arg_name(0, "input")
            elif output is not None:
                title = inspect_arg_name(1, "output")
        (input, output, title) = _setup_iot(input, output, title)
        return func(self, input, output, title, *args, **kwargs)

    return inner


def preset_format(func):
    def inner(self, *kargs, **kwargs):
        keys = ["multiline", "type"]

        format = Format()

        for key in keys:
            if key in kwargs:
                setattr(format, key, kwargs[key])
                kwargs.pop(key)

        self.format = format
        return func(self, *kargs, **kwargs)

    return inner
