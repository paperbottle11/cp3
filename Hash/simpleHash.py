
class SimpleHashTable:
    def __init__(self, size=10, resizing=True):
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0
        self.DELETED = object()
    def _upsize(self):
        new_table = SimpleHashTable(len(self.keys) * 2)
        for k, v in zip(self.keys, self.values):
            if k != None and k != self.DELETED:
                new_table[k] = v
        self.keys = new_table.keys
        self.values = new_table.values
    def _find_index(self, key, add_mode=False):
        L = len(self.keys)
        position = hash(key) % L
        i = 1
        while self.keys[position] != None and self.keys[position] != key and (not add_mode or self.keys[position] != self.DELETED):
            position += i * i
            position %= L
            i += 1
        return position
    def __setitem__(self, key, value):
        if type(key) == list or type(key) == dict or type(key) == set:
            raise TypeError("The key must be immutable.")
        if 10*self.count > 7*len(self.keys):
            self._upsize()
        position = self._find_index(key, add_mode=True)
        if not self.keys[position]:
            self.count += 1
        self.keys[position] = key
        self.values[position] = value
    def __contains__(self, key):
        position = self._find_index(key)
        return self.keys[position] == key
    def __getitem__(self, key):
        position = self._find_index(key)
        if self.keys[position] == key:
            return self.values[position]
        else:
            raise KeyError(f"The key \"{key}\" doesn't exist.")
    def __delitem__(self, key):
        position = self._find_index(key)
        if self.keys[position] != None:
            self.keys[position] = self.DELETED
            self.count -= 1
    def __len__(self):
        return self.count
    def __str__(self):
        return str({k: v for k, v in zip(self.keys, self.values) if k != None and k != self.DELETED})

# Testing
if __name__ == "__main__":
    import time
    import math

    run_time = 0
    print("size,run_time")
    i = 2
    while run_time < 15:
        start = time.perf_counter()
        t = {}
        for j in range(i):
            if j % 2 == 0:
                t[j] = 100
            else:
                t[j] = "hello"
        run_time = time.perf_counter() - start
        print(f"{i},{run_time}")
        i = math.ceil(i * 1.10)
