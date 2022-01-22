from unittest.mock import MagicMock
import time
from ..runner import Runner, run_script, execute_script_in_thread

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
    runner.log_view.write_message.assert_called_once_with("123\n")


def test_runner_run_confirm():
    runner = Runner("--ask-confirm".split())
    runner.run(ECHO_SCRIPT)


def test_runner_run_notify():
    runner = Runner("--notify".split())
    runner.run(ECHO_SCRIPT)


def test_run_script():
    run_script(ECHO_SCRIPT)


def test_execute_script_in_thread():
    proxy = execute_script_in_thread(ECHO_SCRIPT)
    messages = []
    while True:
        proxy.acquire()
        is_finished = proxy.is_finished
        if len(proxy.messages) > 0:
            messages = messages + proxy.messages
            proxy.messages = []
        proxy.release()
        if is_finished:
            break
        time.sleep(0.1)

    assert messages == ["123\n"]
