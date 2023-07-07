import threading
import subprocess
import asyncio
import time
from enum import Enum

SHELL = "/bin/bash"


class RunTask:
    def __init__(self):
        self.script = ""
        self.threads = []

    def __call__(self, output=print, flush=None):
        mutex = threading.Lock()
        pending_messages = []
        running = True
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        def worker():
            nonlocal running
            nonlocal pending_messages
            nonlocal loop
            nonlocal future
            try:
                process = subprocess.Popen(
                    self.script,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    universal_newlines=True,
                    executable=SHELL,
                )
                self.process = process
                for line in process.stdout:
                    mutex.acquire()
                    pending_messages.append(line)
                    mutex.release()
            except Exception as e:
                self.process_finish_messages.append(str(e))

            self.exit_code = process.poll()
            mutex.acquire()
            running = False
            mutex.release()

        def writer():
            nonlocal running
            nonlocal pending_messages
            nonlocal output
            while running:
                time.sleep(0.1)
                mutex.acquire()
                if len(pending_messages) > 0:
                    for message in pending_messages:
                        output(message)
                    if flush is not None:
                        flush()
                    pending_messages = []
                mutex.release()

            loop.call_soon_threadsafe(future.set_result, self.exit_code)

        worker_thread = threading.Thread(target=worker, args=())
        worker_thread.start()

        writer_thread = threading.Thread(target=writer, args=())
        writer_thread.start()
        self.threads = [worker_thread, writer_thread]

        return future

    def kill(self):
        self.process.kill()
        for thread in self.threads:
            thread.join()
