import inspect
import re


def is_varible_name(name: str):
    pattern = re.compile(r"[_a-zA-Z_][a-zA-Z0-9_]*")
    match = pattern.match(name)
    if match is None or match.end() != len(name):
        return False
    return True


def inspect_arg_name(pos: int, name: str):
    try:
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[2]
        frame_string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = frame_string[frame_string.find("(") + 1 : -1].split(",")
        args = [arg.strip() for arg in args]
        keyword = {}
        for arg in args:
            token = arg.split("=")
            if len(token) != 2:
                continue
            key = token[0].strip()
            if is_varible_name(key) is False:
                continue
            value = token[1].strip()
            if is_varible_name(value) is False:
                continue
            keyword[key] = value
        if name in keyword:
            return keyword[name]
        else:
            ret = args[pos]
            if is_varible_name(ret) is False:
                return None
            return args[pos]
    except Exception:
        return None
