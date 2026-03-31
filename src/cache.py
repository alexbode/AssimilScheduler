class Cache:
    def __init__(self):
        self.cache = {}

    def has(self, key):
        return key in self.cache

    def get(self, key):
        return self.cache.get(key, []).copy()

    def set(self, key, value: list):
        self.cache[key] = value.copy()

    def delete(self, key):
        del self.cache[key]

    def clear(self):
        self.cache = {}

    def keys(self):
        return self.cache.keys()