from unittest.mock import MagicMock
from ..runner import Runner, run_script

ECHO_SCRIPT = "echo 123"


def test_runner_run_confirm():
    runner = Runner("--ask-confirm".split())
    runner.run(ECHO_SCRIPT)


def test_runner_run_notify():
    runner = Runner("--notify".split())
    runner.run(ECHO_SCRIPT)


def test_run_script():
    run_script(ECHO_SCRIPT)
