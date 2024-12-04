from urllib3.util.util import to_str

class HashMap:
    def __init__(self, size=100):
        self.size = size
        self.map = [None] * size
        self.frequency_map = {}

    def _hash(self, key):
        #Compute the index for a given key using a hash function for strings
        p = 31 # Prime number
        hash_value = 0
        for i, char in enumerate(key):
            hash_value = (hash_value + (ord(char) * (p ** i))) % (self.size)
        return hash_value

    def insert(self, key, value):
        """
        Insert or update a key-value pair into the hash map.
        Tracks frequency of (year-popularity) pairs for heatmap.
        """

        formatted_key = to_str(key.split("-")[0]) + "-" + str(value)

        # Insert the key-value pair into the hash map
        index = self._hash(formatted_key)
        if self.map[index] is None:
            self.map[index] = [(formatted_key, value)]  # Store popularity as value
        else:
            for i, (existing_key, existing_value) in enumerate(self.map[index]):
                if existing_key == formatted_key:
                    break
            else:
                self.map[index].append((formatted_key, value))  # Add new pair if not found

        # Update frequency map (tracking popularity by year)
        self.frequency_map[formatted_key] = self.frequency_map.get(formatted_key, 0) + 1

    def get_frequency(self):
        return self.frequency_map

    def __str__(self):
        return str(self.map)
