from .inputoutputmixin import InputObjectMixin


class ScaffoldVar(InputObjectMixin):
    def validate(self, value=None, defaults=None):
        if value is not None:
            return value
        if defaults is None:
            return None

        if isinstance(defaults, str):
            return defaults
        elif isinstance(defaults, list):
            return defaults[0]

        return None
