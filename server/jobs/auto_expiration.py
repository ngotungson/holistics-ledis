from storage import *
import random

def auto_expiration():
    keys = storage.keys()
    c_keys, n_key_expired = [], 0
    while True:
        while len(c_keys) != 20 and len(c_keys) != len(keys):
            c_key = str(random.choice(keys))
            if c_key not in c_keys:
                c_keys.append(c_key)
                if check_expiration(c_key):
                    n_key_expired += 1

        if n_key_expired <= len(c_keys)/4 or n_key_expired == len(c_keys):
            break
        else:
            keys = storage.keys()
            c_keys, n_key_expired = [], 0
    print storage
