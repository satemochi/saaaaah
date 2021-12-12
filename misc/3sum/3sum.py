from itertools import combinations
from math import log
from random import seed, uniform 
from numpy.fft import rfft, irfft


def solve_3sum_exhaustively(a):
    return any(x + y + z == 0 for x, y, z in combinations(a, 3))


def solve_3sum_with_hash(a):
    assert(all(isinstance(ai, int) for ai in a))
    s = {v: i for i, v in enumerate(a)}
    return any(-x-y in s for x, y in combinations(a, 2))


def solve_3sum_with_fft(a):
    assert(len(a) == len(set(a)))   # uniqueness
    assert(all(isinstance(ai, int) for ai in a))
    c = [0] * (max(a)+(b := -min(a)+1)+1)
    for ai in a:
        c[ai + b] = 1
    t = {i-b for i, mi in enumerate(__pm_fft(c, c)) if mi > 0}
    return any(-ai in t for ai in a)


def __pm_fft(a, b):
    length = 1 << int(log(len(a)+len(b)+1, 2))
    a_f, b_f = rfft(a, length), rfft(b, length)
    c_f = [ai*bi for ai, bi in zip(a_f, b_f)]
    return [int(ci) for ci in irfft(c_f, length)]


def solve_3sum_by_serious_comparisons(a):
    b = sorted(a)
    for i in range((n := len(b)) - 2):
        x, start, end = a[i], i + 1, n - 1
        while start < end:
            y, z = a[start], a[end]
            if x + y + z == 0:
                print(x, y, z)
                return True
            elif s > 0:
                end -= 1
            else:
                start += 1
    return False


def gen(n=15, domain=(-100, 100), s=0):
    seed(s)
    return list(set([int(uniform(*domain)) for i in range(n)]))


if __name__ == '__main__':
    a = gen(n=100, domain=(d:=(-100, 100)))
    print(a)
    print(solve_3sum_exhaustively(a))
    print(solve_3sum_with_hash(a))
    print(solve_3sum_by_serious_comparisons(a))

#    plt.scatter(range(len(a)), a)

#    triple = next(solve_3sum_with_hash(a))
#    plt.scatter(triple, [a[i] for i in triple], color='r', zorder=10)
#    for t in solve_3sum_with_hash(a):
#        print(t, [a[i] for i in t])

#    triple = next(solve_3sum(a))
#    plt.scatter([a.index(i) for i in triple], triple, color='r', zorder=10)
#    for t in solve_3sum(a):
#        print(t)

#    plt.gca().set_xlim(-1, len(a))
#    plt.gca().set_ylim(*d)
#    plt.tight_layout()
#    plt.show()
