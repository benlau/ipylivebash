from typing import Callable, Optional, List, Union
from abc import ABC
from dataclasses import dataclass


@dataclass
class IOOptions:
    """
    That is the options passed for input-output processing function
    """

    # For reporting the progress
    print_line: Optional[Callable[[str], None]] = None

    # Shared storage between input and output
    shared_storage: Optional[dict] = None

    source: Optional[Union[List["InputObject"], "InputObject"]] = None


def _normalize_defaults(defaults):
    if isinstance(defaults, str):
        ret = defaults
    elif isinstance(defaults, list):
        ret = defaults[0]
    return ret


class InputObject(ABC):
    """
    InputObject
    """

    def __str__(self):
        return self.to_string()

    def to_string(self, options: IOOptions = None) -> str:
        ret = self.read(options=options)
        if ret is None and self.defaults is not None:
            ret = _normalize_defaults(self.defaults)
        return ret if ret is not None else ""

    def read(self, options: IOOptions = None) -> Optional[str]:
        """
        Read raw value
        """
        raise NotImplementedError()


class OutputObject(ABC):
    def __call__(self, value=None, options: IOOptions = None):
        self.write(value, options=options)

    def write(self, value=None, options: IOOptions = None):
        raise NotImplementedError()


class IOMixin(InputObject, OutputObject):
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
