from storage import *

class SetCommand(object):
    def __init__(self, ins, params):
        self.ins = ins
        self.params = params

    def run(self):
        key = self._get_key()

        if self.ins == "SADD":
            new_values = set(self.params[1:])
            return self._sadd(key, new_values)
        elif self.ins == "SCARD":
            new_values = self.params[1:]
            return self._scard(key)
        elif self.ins == "SMEMBERS":
            return self._smembers(key)
        elif self.ins == "SREM":
            delete_values = self.params[1:]
            return self._srem(key, delete_values)
        elif self.ins == "SINTER":
            key_list = self.params[0:]
            return self._sinter(key_list)

    def _get_key(self):
        return self.params[0]

    def _get_value(self, key):
        value = storage[key] if key in storage else set()
        if type(value) is not set:
            raise Exception("Operation against a key holding the wrong kind of value")
        return value

    def _sadd(self, key, new_values):
        value = self._get_value(key)
        n_added_elm = len(new_values.difference(value))
        value.update(new_values)
        storage[key] = value
        return n_added_elm

    def _scard(self, key):
        value = self._get_value(key)
        return len(value)

    def _smembers(self, key):
        value = self._get_value(key)
        return value

    def _srem(self, key, delete_values):
        value = self._get_value(key)
        count = 0
        for delete_value in delete_values:
            if delete_value in value:
                value.discard(delete_value)
                count += 1
        return count

    def _sinter(self, key_list):
        inter_reducer = lambda x, y: x.intersection(y)
        return reduce(inter_reducer, map(self._get_value, key_list))
