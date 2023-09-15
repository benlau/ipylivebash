from ..sessionmanager import SessionManager
import pytest

ECHO_SCRIPT = "echo 123"


def test_create_session():
    manager = SessionManager()
    session = manager.create_session()
    assert session is not None
    assert manager.sessions[0].id == session.id


@pytest.mark.asyncio
async def test_run_session():
    manager = SessionManager()
    session = manager.create_session()
    session.script = ECHO_SCRIPT
    messages = []

    def pr(message):
        messages.append(message)

    await manager.run_session(session, print_line=pr)
    assert len(messages) == 1
    assert messages[0] == "123\n"
    assert session.exit_code == 0


@pytest.mark.asyncio
async def test_session_run_should_strip_stopped_session():
    manager = SessionManager()

    def pr(_message):
        pass

    for i in range(0, 12):
        session = manager.create_session()
        session.script = ECHO_SCRIPT

        await manager.run_session(session, print_line=pr)

    assert len(manager.sessions) == 10
    assert manager.sessions[0].id == "instance0003"


@pytest.mark.asyncio
async def test_session_run_support_env():
    manager = SessionManager()

    messages = []

    def pr(message):
        messages.append(message)

    session = manager.create_session()
    session.script = """\
echo $TEST_ENV
"""
    env = {"TEST_ENV": "123456"}
    await manager.run_session(session, print_line=pr, env=env)

    assert len(messages) == 1
    assert messages[0] == "123456\n"
    assert session.exit_code == 0
