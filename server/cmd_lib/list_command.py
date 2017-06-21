from storage import *

class ListCommand(object):
    def __init__(self, ins, params):
        self.ins = ins
        self.params = params

    def run(self):
        key = self._get_key()

        if self.ins == "LLEN":
            return self._llen(key)
        elif self.ins == "RPUSH":
            new_values = self.params[1:]
            return self._rpush(key, new_values)
        elif self.ins == "LPOP":
            return self._lpop(key)
        elif self.ins == "RPOP":
            return self._rpop(key)
        elif self.ins == "LRANGE":
            start, stop = self.params[1], self.params[2]
            return self._lrange(key, start, stop)

    def _get_key(self):
        return self.params[0]

    def _get_value(self, key):
        value = storage[key] if key in storage else []
        if type(value) is not list:
            raise Exception("Operation against a key holding the wrong kind of value")
        return value

    def _llen(self, key):
        value = self._get_value(key)
        return len(value)

    def _rpush(self, key, new_values):
        value = self._get_value(key)
        value.extend(new_values)
        storage[key] = value
        return len(value)

    def _lpop(self, key):
        value = self._get_value(key)
        if len(value) > 0:
            first_elm = value[0]
            del value[0]
            storage[key] = value
            return first_elm
        else:
            return "nil"

    def _rpop(self, key):
        value = self._get_value(key)
        if len(value) > 0:
            last_elm = value[-1]
            del value[-1]
            storage[key] = value
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
