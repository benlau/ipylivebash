from ..exp.scaffold.jsonfilevar import JsonFileVar
from tempfile import NamedTemporaryFile
import json
import textwrap


def write_to_tmp(dict):
    tmp_file = NamedTemporaryFile(delete=False)
    content = json.dumps(dict)
    tmp_file.write(bytes(content, "utf-8"))
    tmp_file.close()
    return tmp_file.name


def test_jsonfilevar_read_from_file():
    source = write_to_tmp({"A": {"B": {"C": "value"}}})
    variable = JsonFileVar(source, "A.B.C")
    assert variable.read() == "value"


def test_jsonfilevar_write_to_file():
    source = write_to_tmp({"A": {"B": {"C": "value"}}})
    variable = JsonFileVar(source, "A.B.C", indent=4)
    variable.write("new_value")

    with open(source, "r") as file:
        content = file.read()
        assert content == textwrap.dedent(
            """\
        {
            "A": {
                "B": {
                    "C": "new_value"
                }
            }
        }"""
        )
