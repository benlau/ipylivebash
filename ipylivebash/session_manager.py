from .session import Session
import asyncio

instance = None


async def run_script(script):
    """
    Run script via Python API.
    """

    def pr(message):
        print(message.strip())

    manager = SessionManager.get_instance()
    session = manager.create_session()
    session.script = script
    try:
        return await session.run(print=pr)
    except asyncio.CancelledError:
        session.kill()
        print("Force terminated")


class SessionManager:
    def __init__(self):
        self.sessions = []
        self.next_id = 1

    def create_session(self):
        session = Session()
        session.id = self.next_id
        self.next_id = self.next_id + 1
        self.sessions.append(session)
        return session

    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = SessionManager()
        return instance
