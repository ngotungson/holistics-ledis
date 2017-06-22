from storage import *
from base_command import BaseCommand

class ListCommand(BaseCommand):
    def __init__(self, ins, params=[]):
        BaseCommand.__init__(self, ins, params)

    def run(self):
        if self.ins == "LLEN":
            key = self._get_key()
            return self._llen(key)

        elif self.ins == "RPUSH":
            key, new_values = self._get_key(), self.params[1:]
            return self._rpush(key, new_values)

        elif self.ins == "LPOP":
            key = self._get_key()
            return self._lpop(key)

        elif self.ins == "RPOP":
            key = self._get_key()
            return self._rpop(key)

        elif self.ins == "LRANGE":
            key, start, stop = self._get_key(), self.params[1], self.params[2]
            return self._lrange(key, start, stop)


    def _llen(self, key):
        value = self._get_value(key)
        return len(value)

    def _rpush(self, key, new_values):
        value = self._get_value(key)
        value.extend(new_values)
        if key not in storage: initialize_key(key)
        storage[key]["value"] = value
        return len(value)

    def _lpop(self, key):
        value = self._get_value(key)
        if len(value) > 0:
            first_elm = value[0]
            del value[0]
            storage[key]["value"] = value
            return first_elm
        else:
            return "nil"

    def _rpop(self, key):
        value = self._get_value(key)
        if len(value) > 0:
            last_elm = value[-1]
            del value[-1]
            storage[key]["value"] = value
            return last_elm
        else:
            return "nil"

    def _lrange(self, key, start, stop):
        value = self._get_value(key)
        start, stop = int(start), int(stop)
        if start > stop:
            return []
        else:
            start, stop = start, stop + 1 # Get stop index
        return value[start:stop]

    def _get_value(self, key):
        if key in storage:
            check_expiration(key)
            value = storage[key]["value"]
            if type(value) is not list:
                raise Exception("Operation against a key holding the wrong kind of value")
        else:
            value = list()
        return value
