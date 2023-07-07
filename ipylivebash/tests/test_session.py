from ..session import Session
import pytest

ECHO_SCRIPT = "echo 123"


@pytest.mark.asyncio
async def test_session_run():
    session = Session()
    session.script = ECHO_SCRIPT
    messages = []

    def pr(message):
        messages.append(message)

    await session.run(output=pr)
    assert len(messages) == 1
    assert messages[0] == "123\n"
