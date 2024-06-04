from collections import defaultdict
from random import random, seed
from matplotlib import pyplot as plt


class sparse_table:
    def __init__(self, a):
        self.__st = self.__cheat_sheet(a)

    def __cheat_sheet(self, a):
        s = {i: {0: (ai, i)} for i, ai in enumerate(a)}
        n, k = len(a), self.__lg(len(a))
        for i in range(1, k+1):
            for j in range(n - (1 << i) + 1):
                s[j][i] = min(s[j][i-1], s[j + (1 << (i-1))][i-1])
        return s

    @staticmethod
    def __lg(x):
        assert isinstance(x, int)
        return x.bit_length() - 1

    def query(self, _l, _r):
        assert 0 <= _l and _l < _r and _r < len(self.__st)
        i = self.__lg(_r - _l + 1)
        return min(self.__st[_l][i], self.__st[_r - (1 << i) + 1][i])


def hello(a, _l, _r):
    assert 0 <= _l and _l < _r and _r < len(a)
    return min((ai, i) for i, ai in enumerate(a[_l:_r+1], start=_l))[1]


def gen(n=10, _seed=0):
    seed(_seed)
    return [random() for i in range(n)]


if __name__ == '__main__':
    a = gen()
    from pprint import pprint
    pprint(a)
    plt.scatter(range(len(a)), a)

    l, r = 4, 7
    _argmin = hello(a, l, r)
    print(_argmin)

    s = sparse_table(a)
    print(s.query(l, r))

    plt.scatter([_argmin,], [a[_argmin],], c='r')
    plt.plot([l, r], [0, 0], c='g')
    plt.savefig('sparse_table_ex01.png', bbox_inches='tight')

    plt.tight_layout()
    plt.show()
