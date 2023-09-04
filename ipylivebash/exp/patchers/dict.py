import copy


class PatchDict:
    def __init__(self):
        pass

    def read(self, object, path):
        keys = path.split(".")
        current = object
        for key in keys:
            if key not in current:
                return None
            if type(current) is dict:
                current = current[key]
            else:
                return None

        value = str(current)
        return value

    def write(self, object, path, value):
        keys = path.split(".")
        copied = copy.deepcopy(object)
        if type(copied) is not dict:
            copied = {}
        parent = None
        last_key = None
        current = copied
        for key in keys[:-1]:
            if type(current) is not dict:
                current = {}
                parent[last_key] = current
            if key not in current:
                current[key] = {}
            last_key = key
            parent = current
            current = current[key]

        current[keys[-1]] = value
        return copied
