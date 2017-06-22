from storage import *
from base_command import BaseCommand

class StringCommand(BaseCommand):
    def __init__(self, ins, params=[]):
        BaseCommand.__init__(self, ins, params)

    def run(self):
        if self.ins == "GET":
            key = self._get_key()
            return self._get(key)

        elif self.ins == "SET":
            key, new_value = self._get_key(), self.params[1]
            return self._set(key, new_value)


    def _set(self, key, value):
        if key not in storage: initialize_key(key)
        storage[key]["value"] = value
        return "OK"

    def _get(self, key):
        if key in storage:
            value = storage[key]["value"]
            if type(value) is not str:
                raise Exception("Operation against a key holding the wrong kind of value")
        else:
            raise Exception("Key not found")
        return value
