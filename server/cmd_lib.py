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
