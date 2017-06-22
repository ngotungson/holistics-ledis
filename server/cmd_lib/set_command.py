from storage import *
from base_command import BaseCommand

class SetCommand(BaseCommand):
    def __init__(self, ins, params=[]):
        BaseCommand.__init__(self, ins, params)

    def run(self):
        if self.ins == "SADD":
            key, new_values = self._get_key(), set(self.params[1:])
            return self._sadd(key, new_values)

        elif self.ins == "SCARD":
            key, new_values = self._get_key(), self.params[1:]
            return self._scard(key)

        elif self.ins == "SMEMBERS":
            key = self._get_key()
            return self._smembers(key)

        elif self.ins == "SREM":
            key, delete_values = self._get_key(), self.params[1:]
            return self._srem(key, delete_values)

        elif self.ins == "SINTER":
            key_list = self.params[0:]
            return self._sinter(key_list)


    def _sadd(self, key, new_values):
        value = self._get_value(key)
        n_added_elm = len(new_values.difference(value))

        value.update(new_values)
        if key not in storage: initialize_key(key)
        storage[key]["value"] = value

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

        if key not in storage: initialize_key(key)
        storage[key]["value"] = value

        return count

    def _sinter(self, key_list):
        inter_reducer = lambda x, y: x.intersection(y)
        return reduce(inter_reducer, map(self._get_value, key_list))

    def _get_value(self, key):
        if key in storage:
            check_expiration(key)
            value = storage[key]["value"]
            if type(value) is not set:
                raise Exception("Operation against a key holding the wrong kind of value")
        else:
            value = set()
        return value
