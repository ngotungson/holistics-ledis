from storage import *
import math

class BaseCommand(object):
    PARAM_NUMBER = {
        'SET': 2,
        'GET': 1,
        'LLEN': 1,
        'RPUSH': -1.2, # -1 means cmd can take infinite params and 1.x means cmd needs at least x params
        'LPOP': 1,
        'RPOP': 1,
        'LRANGE': -1.3,
        'SADD': -1.2,
        'SCARD': 1,
        'SMEMBERS': 1,
        'SREM': -1.2,
        'SINTER': -1.0,
        'KEYS': 0,
        'DEL': 1,
        'FLUSHDB': 0,
        'EXPIRE': 2,
        'TTL': 1,
        'SAVE': 0,
        'RESTORE': 0
    }

    def __init__(self, ins, params=[]):
        self.ins = ins
        self.params = params
        self._validate_params_number()

    def _get_key(self):
        key = self.params[0]
        if key in storage: check_expiration(key)
        return key

    def _validate_params_number(self):
        ins = self.ins.upper()
        correct_param_number = BaseCommand.PARAM_NUMBER[ins]
        if isinstance(correct_param_number, int):
            if len(self.params) != correct_param_number:
                raise Exception("Wrong number of parameters")

        elif isinstance(correct_param_number, float):
            min_param_number = (correct_param_number - math.ceil(correct_param_number)) * (-10)
            if len(self.params) < min_param_number:
                raise Exception("Wrong number of parameters")
