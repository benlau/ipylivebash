from unittest.mock import MagicMock
from ..runner import Runner, run_script

ECHO_SCRIPT = "echo 123"


def test_runner_parse_args():
    runner = Runner("--help".split())
    assert runner.args.print_help is True
    assert runner.args.keep_cell_output is False

    runner = Runner("--keep-cell-output".split())
    assert runner.args.keep_cell_output is True


def test_runner_run():
    runner = Runner("")
    runner.log_view = MagicMock()
    runner.run(ECHO_SCRIPT)
    runner.log_view.write_line.assert_called_once_with("123\n")


def test_runner_run_confirm():
    runner = Runner("--ask-confirm".split())
    runner.run(ECHO_SCRIPT)


def test_runner_run_notify():
    runner = Runner("--notify".split())
    runner.run(ECHO_SCRIPT)


def test_run_script():
    run_script(ECHO_SCRIPT)
