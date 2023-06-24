from time import time


def debounce(wait):
    def decorator(fn):
        time_of_last_call = None

        def debounced(*args, **kwargs):
            nonlocal time_of_last_call

            if time_of_last_call is None:
                time_of_last_call = time()
                return
            time_since_last_call = time() - time_of_last_call
            if time_since_last_call < wait:
                return
            time_of_last_call = time()
            fn(*args, **kwargs)

        return debounced

    return decorator
