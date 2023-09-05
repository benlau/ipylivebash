from ..patchers.dict import PatchDict
from .scaffoldvar import ScaffoldVar
from collections import OrderedDict
import json


class JsonFileVar(ScaffoldVar):
    def __init__(
        self, file_name, variable_name, default_variable_value=None, indent=None
    ):
        self.file_name = file_name
        self.variable_name = variable_name
        self.patcher = PatchDict()
        self.default_variable_value = default_variable_value
        self.indent = indent

    def write_message(self, value):
        return f"Set {self.variable_name}={value} to {self.file_name}"

    def write(self, value):
        content = self._read_json_from_file()
        if content is None:
            content = {}
        new_content = self.patcher.write(content, self.variable_name, value)
        file = open(self.file_name, "w")
        file.write(json.dumps(new_content, indent=self.indent))
        file.close()

    def read(self):
        content = self._read_json_from_file()
        if content is None:
            return self.default_variable_value
        value = self.patcher.read(content, self.variable_name)
        if value is None:
            return self.default_variable_value
        return value

    def _read_json_from_file(self):
        try:
            file = open(self.file_name, "r")
            content = file.read()
            file.close()

            json_content = json.loads(content, object_pairs_hook=OrderedDict)
            return json_content
        except FileNotFoundError:
            return None
