from pprint import pprint
from random import randbytes, seed
from unittest import TestCase, main


""" Tornado Tabulation Hashing
    for 32-bit key, alphabet := [2**8], c = 4, d = 4, then
        array size = 2**24.
"""
seed(1)
_h = {i: {j: int.from_bytes(randbytes(8), 'little') for j in range(256)}
      for i in range(8)}


def tornado(x):
    assert x >> 32 == 0
    h, c = 0, 0
    for i in range(3):
        c = x
        x >>= 8
        h ^= _h[i][c & 0xff]
    h ^= x
    for i in range(4, 8):
        c = h
        h >>= 8
        h ^= _h[i][c & 0xff]
    return h & ((1 << 24) - 1)


class test_tornado_hashing(TestCase):
    def test_hash_value(self):
        for i in range(1 << 20):
            self.assertTrue(tornado(i) >> 24 == 0)


if __name__ == '__main__':
    # main()
    from collections import defaultdict, Counter
    a = defaultdict(int)
    for i in range(n := 1 << 20):
        a[tornado(i)] += 1
    tab = [v for v in a.values()]
    print(c := Counter(tab))

    from matplotlib import pyplot as plt
    _, (ax, ax2, ax3) = plt.subplots(3, 1, sharex=False, facecolor='w')
    ax.bar(c.keys(), c.values(), width=0.4)
    ax2.bar(c.keys(), c.values(), width=0.4)
    ax3.bar(c.keys(), c.values(), width=0.4)
    ax.set_ylim(c[1]-c[2], c[1]+10000)
    ax2.set_ylim(c[2]-c[3], c[2]+1000)
    ax3.set_ylim(0, c[3]+200)
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax.set_xticks([], minor=False)
    ax2.set_xticks([], minor=False)
    ax3.set_xticks(list(c.keys()), minor=False)
    # plt.savefig('tornado_hashing_ex1.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
