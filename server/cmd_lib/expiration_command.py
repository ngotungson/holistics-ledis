from storage import *

class ExpirationCommand(object):
    def __init__(self, ins, params):
        self.ins = ins
        self.params = params

    def run(self):
        if self.ins == "KEYS":
            return self._keys()
        elif self.ins == "DEL":
            key = self._get_key()
            return self._del(key)
        elif self.ins == "FLUSHDB":
            return self._flushdb()
        elif self.ins == "EXPIRE":
            key, timeout = self._get_key(), self.params[1]
            return self._expire(key, timeout)
        elif self.ins == "TTL":
            key = self._get_key()
            return self._ttl(key)

    def _keys(self):
        for key in storage.keys():
            check_expiration(key)
        return storage.keys()

    def _del(self, key):
        if key in storage:
            del storage[key]
            return "Deleted"
        else:
            raise Exception("Key not found")

    def _flushdb(self):
        storage.clear()
        return "Flushed db"

    def _expire(self, key, timeout):
        if key in storage:
            add_expiration(key, timeout)
            return "Added expiration"
        else:
            raise Exception("Key not found")

    def _ttl(self, key):
        if key in storage:
            if storage[key].has_key("expiration"):
                return time_to_live(key)
            else:
                return "Timeout not found"
        else:
            raise Exception("Key not found")

    def _get_key(self):
        key = self.params[0]
        if key in storage: check_expiration(key)
        return key
