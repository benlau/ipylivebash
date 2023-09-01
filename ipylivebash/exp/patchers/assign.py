import re
from typing import (
    Pattern,
)

# Reference
# https://github.com/theskumar/python-dotenv/blob/main/src/dotenv/parser.py


def make_regex(string: str, extra_flags: int = 0) -> Pattern[str]:
    return re.compile(string, re.UNICODE | extra_flags)


_multiline_whitespace = make_regex(r"\s*", extra_flags=re.MULTILINE)
_key = make_regex(r"[a-zA-Z_][a-zA-Z0-9_\.]*")  # Support dot for other format
_equal_sign = make_regex(r"(=[^\S\r\n]*)")
_single_quoted_value = make_regex(r"'((?:\\'|[^'])*)'")
_double_quoted_value = make_regex(r'"((?:\\"|[^"])*)"')
_unquoted_value = make_regex(r"([^\r\n]*)")
_whitespace = make_regex(r"[^\S\r\n]*")
_export = make_regex(r"(?:export[^\S\r\n]+)?")
_comment = make_regex(r"(?:[^\S\r\n]*#[^\r\n]*)?")
_rest_of_line = make_regex(r".*[^\r\n]*(?:\r|\n|\r\n)?")


class PatchAssignment:
    def __init__(
        self,
        equal_sign=_equal_sign,
        multiline_whitespace=_multiline_whitespace,
        key=_key,
        whitespace=_whitespace,
        double_quoted_value=_double_quoted_value,
        single_quoted_value=_single_quoted_value,
        unquoted_value=_unquoted_value,
        export=_export,
        comment=_comment,
        rest_of_line=_rest_of_line,
    ):
        self.equal_sign = equal_sign
        self.multiline_whitespace = multiline_whitespace
        self.key = key
        self.whitespace = whitespace
        self.double_quoted_value = double_quoted_value
        self.single_quoted_value = single_quoted_value
        self.unquoted_value = unquoted_value
        self.export = export
        self.comment = comment
        self.rest_of_line = rest_of_line

    def parse(self, content, pattern):
        match = pattern.match(content)
        if match is None:
            raise ValueError("Invalid format")
        extracted = content[match.start() : match.end()]
        remaining = content[match.end() :]
        return extracted, remaining

    def __call__(self, content, variable, replace: str):
        remaining = content
        ret = ""

        while len(remaining) > 0:
            try:
                extracted, remaining = self.parse_line(remaining, variable, replace)
                ret += extracted
            except ValueError:
                return content

        return ret

    def parse_line(self, content, variable, replace):
        remaining = content
        ret = ""

        try:
            extracted, remaining = self.parse(remaining, self.multiline_whitespace)
            ret += extracted

            extracted, remaining = self.parse(remaining, self.export)
            ret += extracted

            key, remaining = self.parse(remaining, _key)
            ret += key

            extracted, remaining = self.parse(remaining, self.whitespace)
            ret += extracted

            extracted, remaining = self.parse(remaining, self.equal_sign)
            ret += extracted

            extracted, remaining = self.parse(remaining, self.whitespace)
            ret += extracted

            extracted, remaining = self.parse_update_value(
                remaining, replace if key == variable else None
            )
            ret += extracted

            extracted, remaining = self.parse(remaining, self.comment)
            ret += extracted

            return ret, remaining
        except ValueError:
            extracted, remaining = self.parse(content, self.rest_of_line)
            return extracted, remaining

    def parse_update_value(self, content, replace):
        if content.startswith('"'):
            extracted, remaining = self.parse(content, self.double_quoted_value)
            if replace is not None:
                return f'"{replace}"', remaining
        elif content.startswith("'"):
            extracted, remaining = self.parse(content, self.single_quoted_value)
            if replace is not None:
                return f"'{replace}'", remaining
        else:
            extracted, remaining = self.parse(content, self.unquoted_value)
            if replace is not None:
                return replace, remaining
        return extracted, remaining
