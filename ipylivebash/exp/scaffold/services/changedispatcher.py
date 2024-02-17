import weakref


class ChangeDispatcher:
    def __init__(self):
        # It can't use WeakSet because it will be removed in Jupyter environment
        self.listeners = set()

    def add_listener(self, listener):
        self.listeners.add(listener)

    def dispatch(self, type, payload):
        for listener in self.listeners:
            try:
                listener(type, payload)
            except Exception as e:
                self.listeners.remove(listener)


class Listener:
    def __init__(self, type, callback):
        self.type = type
        self.callback = callback

    def __call__(self, type, payload):
        if self.type == type:
            self.callback(payload)


change_dispatcher = ChangeDispatcher()
