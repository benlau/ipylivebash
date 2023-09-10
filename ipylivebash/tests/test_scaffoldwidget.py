from ..exp.scaffold.scaffoldwidget import ScaffoldWidget
from unittest.mock import MagicMock, call


def test_scaffold_widget_execute_list():
    callback = MagicMock()

    widget = ScaffoldWidget()
    widget.execute("input", [callback, callback], MagicMock())

    assert callback.call_count == 2
