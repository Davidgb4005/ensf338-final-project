class HashTable:
    """
    A hash table using separate chaining for collision resolution.
    Supports insert, delete, and lookup operations by a unique key.
    Provides O(1) average-case performance for all operations.

    Attributes:
        capacity : int
            The number of buckets in the table.
        size : int
            The number of key-value pairs currently stored.
        buckets : list
            Array of lists (chains) for collision handling.
    """

    LOAD_FACTOR_THRESHOLD = 0.80

    def __init__(self, capacity=64):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _hash(self, key):
        """
        Computes a bucket index for the given key.

        Args:
            key: The key to hash (str or int).

        Returns:
            int: The bucket index.
        """
        if isinstance(key, str): #hashing for strings
            h = 0
            for i, char in enumerate(key.lower()):
                h += ord(char) * (31 ** i)
            return h % self.capacity
        return hash(key) % self.capacity #hashing for anything else

    def _resize(self):
        """
        Doubles the capacity and rehashes all existing entries.
        Called automatically when load factor exceeds threshold.
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        for chain in old_buckets:
            for key, value in chain:
                self.insert(key, value)

    def insert(self, key, value):
        """
        Inserts a key-value pair. If the key already exists, its value is updated.

        Args:
            key: The unique key (name or ID).
            value: The data to store.
        """
        index = self._hash(key)
        chain = self.buckets[index]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        chain.append((key, value))
        self.size += 1
        if self.size / self.capacity > self.LOAD_FACTOR_THRESHOLD:
            self._resize()

    def delete(self, key):
        """
        Removes the entry with the given key.

        Args:
            key: The key to remove.

        Returns:
            The value that was removed, or None if the key was not found.
        """
        index = self._hash(key)
        chain = self.buckets[index]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self.size -= 1
                return v
        return None

    def lookup(self, key):
        """
        Retrieves the value associated with the given key.

        Args:
            key: The key to look up.

        Returns:
            The stored value, or None if the key is not found.
        """
        index = self._hash(key)
        chain = self.buckets[index]
        for k, v in chain:
            if k == key:
                return v
        return None

    def contains(self, key):
        """
        Checks if a key exists in the table.

        Args:
            key: The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return self.lookup(key) is not None

    def keys(self):
        """Returns a list of all keys in the table."""
        result = []
        for chain in self.buckets:
            for k, v in chain:
                result.append(k)
        return result

    def values(self):
        """Returns a list of all values in the table."""
        result = []
        for chain in self.buckets:
            for k, v in chain:
                result.append(v)
        return result

    def __len__(self):
        return self.size