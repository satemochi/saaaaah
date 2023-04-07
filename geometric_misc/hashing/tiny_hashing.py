from ctypes import Structure, c_ubyte
from math import ceil


"""
    A Hash Table that Uses Less Space Than the Items that it Stores
        by William Kuszmaul's blog (Algorithm Soup)

    Ref. williamkuszmaul/tinyhash/small_hash.cpp (github)
"""


class crazy_hash:
    def __init__(self):
        self.t = [linear_probing() for i in range(256)]

    def insert(self, x):
        self.t[x & 0xff].insert(key(x))

    def contains(self, x):
        return self.t[x & 0xff].contains(key(x))


class linear_probing:
    def __init__(self):
        self.cap, self.size, self.arr = 1, 0, [None]

    def contains(self, x):
        return (k := self.arr[self.__resolve(x)]) is not None and k == x

    def __resolve(self, x):
        i, cap = self.__hash(x), self.cap - 1
        while self.arr[i] is not None and self.arr[i] != x:
            i = i + 1 if i < cap else 0
        return i

    def __hash(self, x):
        h = x.a + (x.b << 8) + (x.c << 16)
        h = (~h) + (h << 21)
        h = h ^ (h >> 24)
        h = (h + (h << 3)) + (h << 8)
        h = h ^ (h >> 14)
        h = (h + (h << 2)) + (h << 4)
        h = h ^ (h >> 28)
        h = h & ((1 << 32) - 1)
        return (h * int(self.cap)) >> 32

    def insert(self, x):
        if (self.arr[(i := self.__resolve(x))] is None or self.arr[i] != x):
            self.size, self.arr[i] = self.size + 1, x
            if self.size > self.cap * 0.9:
                self.__grow()

    def __grow(self):
        new_capacity = ceil(self.size / 0.8)
        assert(new_capacity < 1 << 32)
        old_size = self.size
        self.cap, self.size = new_capacity, 0
        old_array, self.arr = self.arr, [None] * new_capacity
        for x in old_array:
            if x is not None:
                self.insert(x)


class key(Structure):
    _fields_ = [('a', c_ubyte), ('b', c_ubyte), ('c', c_ubyte)]

    def __init__(self, x):
        self.a, self.b, self.c = self._s(x, 24), self._s(x, 16), self._s(x, 8)

    @staticmethod
    def _s(i, w):
        return i >> w & 0xff

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c

    def __ne__(self, other):
        return self.a != other.a or self.b != other.b or self.c != other.c


if __name__ == '__main__':
    table = crazy_hash()
    for i in range(n := int(1e5)):
        table.insert(2 * i)

    for i in range(n):
        assert(table.contains(2 * i))
        assert(not table.contains(2 * i + 1))
