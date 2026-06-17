from unittest import TestCase, main


class segtree:
    """ segment trees for supporing range_sum query
        ref) D. Anderson & D. Woodruff (2022): "Range query data structures",
            https://www.cs.cmu.edu/~15451-f22/lectures/lec08-segtrees.pdf
    """
    __slots__ = ['__hq', '__n']

    def __init__(self, a):
        self.__n = len(a)
        self.__build(a)

    def __build(self, a):   # make binary heap queue
        h = [0] * (self.__n-1) + a
        for i in reversed(range(self.__n-1)):
            h[i] = h[(i << 1)+1] + h[(i+1) << 1]  # agg. of left/right children
        self.__hq = h

    def assign(self, i, x):     # a[i] = x
        diff = x - self.__hq[(u := i + self.__n - 1)]
        self.__hq[u] = x
        while u > 0:
            u = (u - 1) >> 1    # transition to the parent of u
            self.__hq[u] += diff

    def range_sum(self, i, j):  # sum(a[i:j])
        _sum, stack = 0, [(0, 0, self.__n)]
        while stack:
            u, _l, _r = stack.pop()
            if i <= _l and _r <= j:
                _sum += self.__hq[u]    # aggregation of the value in a segment
            else:
                mid = (_l + _r) // 2
                if i >= mid:
                    stack.append(((u+1) << 1, mid, _r))
                elif j <= mid:
                    stack.append(((u << 1)+1, _l, mid))
                else:
                    stack.append(((u+1) << 1, mid, _r))
                    stack.append(((u << 1)+1, _l, mid))
        return _sum


def range_sum(i, j, ps):    # O(1) query time in static ver.
    return ps[j] - ps[i]


def prefix_sum(a):
    from functools import reduce
    return list(reduce(lambda x, i: x + [x[i] + a[i]], range(len(a)), [0]))


class test_range_tree_for_range_sum(TestCase):
    def test_one_pass(self):
        a = [49, 97, 53, 5, 33, 65, 62, 51, 100, 38, 61, 45, 74, 27, 64, 17]
        i, j, ans = 1, 14, 711

        self.assertEqual(sum(a[i:j]), ans)
        self.assertEqual(range_sum(i, j, prefix_sum(a)), ans)
        self.assertEqual(segtree(a).range_sum(i, j), ans)

    def test_assign(self):
        a = [49, 97, 53, 5, 33, 65, 62, 51, 100, 38, 61, 45, 74, 27, 64, 17]
        i, j, ans = 1, 14, 644

        a[8] = 33
        self.assertEqual(sum(a[i:j]), ans)
        t = segtree(a)
        t.assign(8, 33)
        self.assertEqual(t.range_sum(i, j), ans)

    def test_inversion_count(self):
        """ Given a random permutaion of range(n), then return
            sum(1 for i, j in combinations(range(n), 2) if p[i] > p[j]) """
        from itertools import combinations
        from random import seed, shuffle
        n = 1 << 4
        seed(0)
        shuffle((p := list(range(n))))
        ans = sum(1 for i, j in combinations(range(n), 2) if p[i] > p[j])

        t, cnt = segtree([0] * n), 0
        for j in range(n):
            cnt += t.range_sum(p[j], n)
            t.assign(p[j], 1)
        self.assertEqual(ans, cnt)


if __name__ == '__main__':
    main()
