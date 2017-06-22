from datetime import datetime

# main hash table
storage = {}

def initialize_key(key):
    storage[key] = {}

def add_expiration(key, timeout):
    storage[key]["expiration"] = {
        "timeout": timeout,
        "created_at": datetime.now()
    }

def time_to_live(key):
    expiration = storage[key]["expiration"]
    timeout, created_at = expiration["timeout"], expiration["created_at"]
    ttl = int(timeout) - (datetime.now() - storage[key]["expiration"]["created_at"]).seconds
    return ttl if ttl >0 else -1

def check_expiration(key):
    if storage[key].has_key("expiration"):
        if time_to_live(key) == -1:
            del storage[key]
            return True
    return False
