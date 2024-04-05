# 
class HashTablePiece:
    def __init__(self, delete_object, size=10):
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0
        self.isFull = False
        self.DELETED = delete_object
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
        position = self._find_index(key, add_mode=True)
        if self.keys[position] == None:
            self.count += 1
            if 10*self.count > 8*len(self.keys):
                self.isFull = True
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

class IncrementalHashTable:
    def __init__(self, size=10):
        self.DELETED = object()
        self.firstTable = HashTablePiece(self.DELETED, size=size)
        self.secondTable = HashTablePiece(self.DELETED, size=size*3)
        self.useSecondTable = False
        self.moveIndex = 0
    def _swap_tables(self):
        self.firstTable = self.secondTable
        self.secondTable = HashTablePiece(self.DELETED, len(self.firstTable.keys) * 3)
        self.useSecondTable = False
        self.moveIndex = 0
    def _move_to_second_table(self):
        for i in range(self.moveIndex, len(self.firstTable.keys)):
            k = self.firstTable.keys[i]
            if k != None and k != self.firstTable.DELETED:
                self.secondTable[k] = self.firstTable[k]
                del self.firstTable[k]
                self.moveIndex = i + 1
                return
        self._swap_tables()
    def __setitem__(self, key, value):
        if self.useSecondTable:
            self.secondTable[key] = value
            self._move_to_second_table()
        else:
            self.firstTable[key] = value
            if self.firstTable.isFull:
                self.useSecondTable = True   
    def __contains__(self, key):
        if key in self.firstTable: return True
        return key in self.secondTable
    def __getitem__(self, key):
        if key in self.firstTable: return self.firstTable[key]
        return self.secondTable[key]
    def __delitem__(self, key):
        if key in self.firstTable: del self.firstTable[key]
        else: del self.secondTable[key]
    def __len__(self):
        return len(self.firstTable) + len(self.secondTable)
    def __str__(self):
        return str({k: v for k, v in zip(self.firstTable.keys + self.secondTable.keys, self.firstTable.values + self.secondTable.values) if k != None and k != self.DELETED})

if __name__ == "__main__":
    import time
    import math

    run_time = 0
    print("size,run_time")
    i = 2
    while run_time < 15:
        start = time.perf_counter()
        t = IncrementalHashTable()
        for j in range(i):
            if j % 2 == 0:
                t[j] = 100
            else:
                t[j] = "hello"
        run_time = time.perf_counter() - start
        print(f"{i},{run_time}")
        i = math.ceil(i * 1.10)