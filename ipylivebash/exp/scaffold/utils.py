import inspect


def inspect_arg_name(pos: int, name: str):
    try:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[2]
        frame_string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = frame_string[frame_string.find("(") + 1 : -1].split(",")
        args = [arg.strip() for arg in args]
        keyword = {}
        for arg in args:
            if arg.find("=") != -1:
                token = arg.split("=")
                key = token[0].strip()
                value = "=".join(token[1:]).strip()
                keyword[key] = value
        if name in keyword:
            return keyword[name]
        else:
            return args[pos]
    except Exception:
        return None
