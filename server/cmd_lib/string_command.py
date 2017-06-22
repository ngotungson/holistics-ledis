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

    def _set(self, key, value):
        if key not in storage: initialize_key(key)
        storage[key]["value"] = value
        return "OK"

    def _get(self, key):
        try:
            return storage[key]["value"]
        except Exception:
            raise Exception("Key not found")

    def _get_key(self):
        key = self.params[0]
        if key in storage: check_expiration(key)
        return key
