from ..exp.scaffold.envfilevar import EnvFileVar
from tempfile import NamedTemporaryFile


def test_envfile_var_read_not_existed_file():
    var = EnvFileVar("not_existed_file", "var", "default")
    assert var.read() == "default"


def test_envfile_var_write_not_existed_file():
    tmp_file = NamedTemporaryFile(delete=False)

    var = EnvFileVar(tmp_file.name, "A")
    var.write("value")

    file = open(tmp_file.name, "r")
    content = file.read()

    assert content == '\nA="value"'
