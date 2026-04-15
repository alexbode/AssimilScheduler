from src.priority_queue import PriorityQueue


class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> PriorityQueue:
        if key in self.cache:
            return self.cache[key]
        return None

    def set(self, key: str, value: PriorityQueue):
        self.cache[key] = value
