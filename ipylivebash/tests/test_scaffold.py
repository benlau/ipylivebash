from unittest.mock import Mock
from ipylivebash.exp.scaffold.envvar import EnvVar
from ipylivebash.exp.scaffold.formlayout import ApplyToSource
from ipylivebash.exp.scaffold.scaffold import Scaffold, _ScaffoldInterfaceBuilder


def test_scaffold_form_layout():
    interface_builder = _ScaffoldInterfaceBuilder(
        index=0, shared_storage={}, flow=Mock(), output_widget=Mock()
    )
    var1 = EnvVar("VAR1")
    var2 = EnvVar("VAR2")

    context = interface_builder.ask([var1, var2])

    assert context["title"] == None
    assert isinstance(context["layout"].output, ApplyToSource)
