from functools import reduce
from math import ceil, log2 as log
from matplotlib import pyplot as plt, use
#use('module://backend_ipe')


def ilog(n, h=1):
    return reduce(lambda res, _: log(res) if res > 1 else 1, range(h), n)


def alog(n):
    return min((ilog(n, i), i) for i in range(7))[1]


def _n(n, h):
    return ceil(n / ilog(n, h))


if __name__ == '__main__':
    n = 70000
    for h in range(alog(n)+1):
        print(h, n, ilog(n, h), _n(n, h))

    plt.barh(range(alog(n)+1), [_n(n, h) for h in range(alog(n)+1)])
    plt.gca().set_xlim(0, n*1.1)
    plt.gca().set_ylim(0, 8)
#    plt.savefig('iter_log.ipe')
    plt.tight_layout()
    plt.show()
