from collections import defaultdict

class HashMap:
    def __init__(self):
        self.map = defaultdict(int)

    def insert(self, key, value):
        self.map[(key, value)] += 1

    def get_frequency(self):
        return self.map