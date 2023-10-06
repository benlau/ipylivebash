from unittest.mock import Mock
from ipylivebash.exp.scaffold.envvar import EnvVar
from ipylivebash.exp.scaffold.formlayout import ApplyToSource
from ipylivebash.exp.scaffold.scaffold import Scaffold, Block
from ipylivebash.exp.scaffold.context import Context


def test_scaffold_form_layout():
    context = Context(
        column_flow=Mock(),
        print_line=Mock(),
        clear_output=Mock(),
    )
    delegate = Block(
        context,
    )
    var1 = EnvVar("VAR1")
    var2 = EnvVar("VAR2")

    ret = delegate.ask([var1, var2])

    assert ret["title"] == None
    assert isinstance(ret["layout"].output, ApplyToSource)
