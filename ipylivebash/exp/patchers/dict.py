import copy
from collections import OrderedDict


class PatchDict:
    def __init__(self):
        pass

    def read(self, object, path):
        keys = path.split(".")
        current = object
        for key in keys:
            if key not in current:
                return None
            if type(current) in [dict, OrderedDict]:
                current = current[key]
            else:
                return None

        value = str(current)
        return value

    def write(self, object, path, value):
        keys = path.split(".")
        copied = copy.deepcopy(object)
        if type(copied) not in [dict, OrderedDict]:
            copied = {}
        parent = None
        last_key = None
        current = copied
        for key in keys[:-1]:
            if type(current) not in [dict, OrderedDict]:
                current = {}
                parent[last_key] = current
            if key not in current:
                current[key] = {}
            last_key = key
            parent = current
            current = current[key]

        current[keys[-1]] = value
        return copied
