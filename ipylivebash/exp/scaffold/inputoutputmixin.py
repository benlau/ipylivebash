from typing import Callable, Optional
from abc import ABC
from dataclasses import dataclass


@dataclass
class InputOutputOptions:
    print_line: Optional[Callable[[str], None]] = None
    shared_storage: Optional[dict] = None


class InputObject(ABC):
    def __str__(self):
        return self.to_string()

    def to_string(self, options: InputOutputOptions = None) -> str:
        ret = self.read(options=options)
        if ret is None and self.defaults is not None:
            if isinstance(self.defaults, str):
                ret = self.defaults
            elif isinstance(self.defaults, list):
                ret = self.defaults[0]
        return ret if ret is not None else ""

    def read(self, options: InputOutputOptions = None) -> Optional[str]:
        """
        Read raw value
        """
        raise NotImplementedError()


class OutputObject(ABC):
    def __call__(self, value=None, options: InputOutputOptions = None):
        self.write(value, options=options)

    def write(self, value=None, options: InputOutputOptions = None):
        raise NotImplementedError()


class InputObjectMixin(InputObject, OutputObject):
    pass
