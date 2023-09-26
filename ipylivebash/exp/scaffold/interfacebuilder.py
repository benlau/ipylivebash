from abc import ABC


class InterfaceBuilder(ABC):
    def ask(self, input=None, output=None, title=None):
        raise NotImplementedError()
