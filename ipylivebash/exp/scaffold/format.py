from enum import Enum
from typing import Optional, Union


class FormatType(Enum):
    Text = "text"
    File = "file"


class Format:
    def __init__(
        self, type=FormatType.Text, multiline: Optional[Union[bool, int]] = False
    ):
        self.type = type
        self.multiline = multiline
