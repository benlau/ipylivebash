from ..exp.scaffold.envfilevar import EnvFileVar
from tempfile import NamedTemporaryFile


def test_envfile_var_read_not_existed_file():
    var = EnvFileVar("not_existed_file", "var", "default")
    assert var.read() == None
    assert var.to_string() == "default"


def test_envfile_var_write_not_existed_file():
    tmp_file = NamedTemporaryFile(delete=True)
    filename = tmp_file.name
    tmp_file.close()

    var = EnvFileVar(filename, "A")
    var.write("value")

    file = open(tmp_file.name, "r")
    content = file.read()

    assert content == "\nA=value"


def test_envfile_with_defaults_list():
    tmp_file = NamedTemporaryFile(delete=True)
    filename = tmp_file.name
    tmp_file.close()

    var = EnvFileVar(filename, "A", defaults=["1", "2"])
    assert var.read() == None
    assert var.to_string() == "1"
