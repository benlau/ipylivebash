from ..runtask import RunTask
import pytest
import threading


@pytest.mark.asyncio
async def test_runtask_should_print_line_at_main_thread():
    content = []
    is_main_thread = None

    def print_line(line):
        content.append(line)
        nonlocal is_main_thread
        is_main_thread = threading.current_thread() is threading.main_thread()

    script = """\
    echo 1
    echo 2
    echo 3
    """

    runtask = RunTask()
    runtask.script = script
    await runtask(output=print_line)

    assert content == ["1\n", "2\n", "3\n"]
    assert is_main_thread == True
