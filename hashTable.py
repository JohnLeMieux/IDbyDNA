import psutil
import sys

class HashTable:
    def __init__(self):
        self.buckets = 8
        self.initStorage()
        self.size = 0
        self.shouldResize = True
        self.total = 0
        self.max = 0
        self.mostCommon = ''

    def initStorage(self):
        self.storage = []
        for i in range(self.buckets):
            self.storage.append([])
    
    def hash(self, key, buckets):
        hash = 5381
        for i in range(len(key)):
            char = ord(key[i])
            hash = ((hash * 32) + hash) + char
        return hash % buckets

    def insertAndUpdateCounts(self, key):
        self.insert(key, 1)
        self.total += 1
        count = self.getCount(key)
        if count > self.max:
            self.max = count
            self.mostCommon = key

    def insert(self, key, value):
        index = self.hash(key, self.buckets)
        chain = self.storage[index]
        for i in range(len(chain)):
            if chain[i][0] == key:
                chain[i][1] += value
                return
        if psutil.virtual_memory().available < sys.getsizeof([key, value]):
            raise MemoryError('Not enough memory to add ' + key)
        chain.append([key, value])
        self.size += 1
        if self.shouldResize:
            self.resize()

    def getCount(self, key):
        index = self.hash(key, self.buckets)
        chain = self.storage[index]
        for i in range(len(chain)):
            if chain[i][0] == key:
                return chain[i][1]
        return None

    def resize(self):
        loadFactor = self.size / self.buckets
        if loadFactor >= 0.75 and sys.getsizeof(self.storage) * 4 < psutil.virtual_memory().available:
            self.shouldResize = False
            localStorage = []
            self.deepCopy(self.storage, localStorage)
            self.buckets *= 2
            self.initStorage()
            self.size = 0
            self.rehash(localStorage)
            self.shouldResize = True

    def deepCopy(self, globalStorage, localStorage):
        for i in range(len(globalStorage)):
            localStorage.append([])
            chain = globalStorage[i]
            for j in range(len(chain)):
                localStorage[i].append([chain[j][0], chain[j][1]])

    def rehash(self, localStorage):
        for i in range(len(localStorage)):
            chain = localStorage[i]
            for j in range(len(chain)):
                self.insert(chain[j][0], chain[j][1])