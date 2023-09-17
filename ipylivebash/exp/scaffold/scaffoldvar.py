from typing import Optional


class ScaffoldVar:
    def __call__(self, value=None, print_line=None):
        self.write(value)
        if print_line is not None:
            print_line(self.write_message(value))

    def __str__(self):
        ret = self.read()
        if ret is None and self.defaults is not None:
            if isinstance(self.defaults, str):
                ret = self.defaults
            elif isinstance(self.defaults, list):
                ret = self.defaults[0]
        return ret if ret is not None else ""

    def write(self):
        raise NotImplementedError()

    def read(self) -> Optional[str]:
        """
        Read raw value
        """
        raise NotImplementedError()

    def valiate(self, value=None, defaults=None):
        if value is not None:
            return value
        if defaults is None:
            return None

        if isinstance(defaults, str):
            return defaults
        elif isinstance(defaults, list):
            return defaults[0]

        return None
