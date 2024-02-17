from typing import Callable, Optional, List, Union
from abc import ABC
from dataclasses import dataclass
from ..context import Context


def _normalize_defaults(defaults):
    if isinstance(defaults, str):
        ret = defaults
    elif isinstance(defaults, list):
        ret = defaults[0]
    return ret


class InputUnit(ABC):
    """
    InputUnit

    Properties:
    - defaults
    - format
    """

    def __str__(self):
        return self.to_string()

    def to_string(self, context: Context = None) -> str:
        ret = self.read(context=context)
        if ret is None and self.defaults is not None:
            ret = _normalize_defaults(self.defaults)
        return ret if ret is not None else ""

    def read(self, context: Context = None) -> Optional[str]:
        """
        Read raw value. If the value is not set, return None
        """
        raise NotImplementedError()

    def get_id(self):
        raise NotImplementedError()


class OutputUnit(ABC):
    def __call__(self, value=None, context: Context = None):
        self.write(value, context=context)

    def write(self, value=None, context: Context = None):
        raise NotImplementedError()


class IOUnit(InputUnit, OutputUnit):
    def if_none_write_default(self):
        """
        If the current value is none, read the value.
        If it is also none, write default
        """
        if self.defaults is None:
            return

        value = self.read()
        if value is None:
            self.write(_normalize_defaults(self.defaults))
