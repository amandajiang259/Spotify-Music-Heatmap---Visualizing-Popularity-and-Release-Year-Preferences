from collections import defaultdict

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, key, value):
        self.heap.append((key, value))
        self.heap.sort()  # Maintain heap property (inefficient for small demo purposes)

    def get_frequency(self):
        freq = defaultdict(int)
        for key, value in self.heap:
            freq[(key, value)] += 1
        return freq