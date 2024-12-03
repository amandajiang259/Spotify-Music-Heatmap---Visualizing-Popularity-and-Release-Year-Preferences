# from collections import defaultdict
#
# class HashMap:
#     def __init__(self):
#         self.map = defaultdict(int)
#
#     def insert(self, key, value):
#         self.map[(key, value)] += 1
#
#     def get_frequency(self):
#         return self.map

class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.map = [None] * size

    def _hash(self, key):
        """Compute the index for a given key."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert or update a key-value pair."""
        index = self._hash(key)
        if self.map[index] is None:
            self.map[index] = [(key, value)]
        else:
            for pair in self.map[index]:
                if pair[0] == key:
                    pair[1].update(value)  # Merge values if key exists
                    return
            self.map[index].append((key, value))  # Handle collision

    def get(self, key):
        """Retrieve value by key."""
        index = self._hash(key)
        if self.map[index] is not None:
            for pair in self.map[index]:
                if pair[0] == key:
                    return pair[1]
        return None
