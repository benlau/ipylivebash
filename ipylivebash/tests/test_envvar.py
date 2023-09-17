from ..exp.scaffold.envvar import EnvVar
import os


def test_envvar_defaults_is_array():
    var = EnvVar("VALUE_NOT_EXISTED", ["V1", "V2"])

    assert str(var) == "V1"


def test_envvar_write_without_value():
    name = "7ccb192e-4de4-4720-aa65-e3e687e7a5eb"
    var = EnvVar(name, "default")
    var()

    assert os.getenv(name) == "default"
