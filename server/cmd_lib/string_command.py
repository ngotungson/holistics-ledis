from storage import *

class StringCommand(object):
    def __init__(self, ins, params):
        self.ins = ins
        self.params = params

    def run(self):
        key = self._get_key()

        if self.ins == "GET":
            return self._get(key)
        elif self.ins == "SET":
            new_value = self.params[1]
            return self._set(key, new_value)

    def _get_key(self):
        return self.params[0]

    def _set(self, key, value):
        storage[key] = value
        return ""

    def _get(self, key):
        return storage[key]
