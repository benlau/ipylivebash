from ..patchers.dict import PatchDict
from .scaffoldvar import ScaffoldVar
from collections import OrderedDict
import json


class JsonFileVar(ScaffoldVar):
    def __init__(self, filename, key, defaults=None, indent=None):
        self.filename = filename
        self.key = key
        self.patcher = PatchDict()
        self.defaults = defaults
        self.indent = indent

    def write(self, value, options=None):
        content = self._read_json_from_file()
        if content is None:
            content = {}
        new_content = self.patcher.write(content, self.key, value)
        file = open(self.filename, "w")
        file.write(json.dumps(new_content, indent=self.indent))
        file.close()

        if options is not None and options.print_line is not None:
            options.print_line(f"Set {self.key}={value} to {self.filename}\n")

    def read(self, options=None):
        content = self._read_json_from_file()
        if content is None:
            return None
        value = self.patcher.read(content if content is not None else "", self.key)
        if value is None:
            return None
        return value

    def _read_json_from_file(self):
        try:
            file = open(self.filename, "r")
            content = file.read()
            file.close()

            json_content = json.loads(content, object_pairs_hook=OrderedDict)
            return json_content
        except FileNotFoundError:
            return None
