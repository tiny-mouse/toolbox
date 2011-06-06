import hashlib

from bisect import bisect_left, insort_left

def md5_hash(key):
    return hashlib.md5(key).digest()

def sha1_hash(key):
    return hashlib.sha1(key).digest()

class ConsistentRouter(object):
    
    def __init__(self, items, count=500, hash_fn=sha1_hash):
        self.count = count
        self.hash_fn = hash_fn
        self.map = []
        [self.add_item(item) for item in items]
    
    def __item_keys(self, item):
        for x in range(self.count):
            yield self.hash_fn("%s-%d" % (item, x))

    def add_item(self, item):
        for key in self.__item_keys(item):
            insort_left(self.map, (key, item))

    def remove_item(self, item):
        for key in self.__item_keys(item):
            i = bisect_left(self.map, (key, item))
            assert self.map[i][1] == item
            del self.map[i]

    def get_item(self, key):
        h = self.hash_fn(key)
        i = bisect_left(self.map, (h, ""))
        if i >= len(self.map):
            i = 0
        item = self.map[(i)%len(self.map)][1]
        return item
