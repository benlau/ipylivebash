from ..exp.scaffold.envvar import EnvVar


def test_envvar_defaults_is_array():
    var = EnvVar("VALUE_NOT_EXISTED", ["V1", "V2"])

    assert str(var) == "V1"
