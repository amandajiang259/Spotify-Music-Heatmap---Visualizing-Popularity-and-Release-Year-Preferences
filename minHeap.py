class MinHeap:
    def __init__(self):
        self.heap = []
        self.frequency_map = {}

    def push(self, release_date, artist_popularity):
        # Inserts a tuple (release_date, artist_popularity) into the heap and updates frequency map.
        item = (int(release_date.split("-")[0]), artist_popularity)  # Extract year for comparisons
        self.heap.append(item)
        self.frequency_map[item] = self.frequency_map.get(item, 0) + 1
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        # Removes and returns the smallest item from the heap.
        if not self.heap:
            raise IndexError("Heap is empty")
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def _sift_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._sift_up(parent)

    def _sift_down(self, index):
        child1 = 2 * index + 1
        child2 = 2 * index + 2
        smallest = index

        if child1 < len(self.heap) and self.heap[child1] < self.heap[smallest]:
            smallest = child1
        if child2 < len(self.heap) and self.heap[child2] < self.heap[smallest]:
            smallest = child2

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._sift_down(smallest)

    def get_frequency(self):
        # Returns the frequency map with keys as 'year-popularity' strings for compatibility.
        return {f"{key[0]}-{key[1]}": count for key, count in self.frequency_map.items()}

    def is_empty(self):
        # Returns True if the heap is empty, False otherwise.
        return len(self.heap) == 0

    def __str__(self):
        return str(self.heap)
