from copy import copy
from itertools import combinations
from pprint import pprint
from random import random, seed
from matplotlib import pyplot as plt
from smallest_circle import msw


class bounding_rectangle:
    def __init__(self, s):
        self.xmin = min(x for x, _ in s)
        self.xmax = max(x for x, _ in s)
        self.ymin = min(y for _, y in s)
        self.ymax = max(y for _, y in s)
        self.__lmax = max(self.xmax - self.xmin, self.ymax - self.ymin)

    def axis(self):
        x, y = self.xmax - self.xmin, self.ymax - self.ymin
        return (0, self.xmin+x/2) if x > y else (1, self.ymin+y/2)

    def __repr__(self):
        return f'({self.xmin}, {self.ymin}), ({self.xmax}, {self.ymax})'

    def draw(self, ax=None):
        if ax is None:
            ax = plt.gca()
        ax.plot([self.xmin, self.xmax, self.xmax, self.xmin, self.xmin],
                [self.ymin, self.ymin, self.ymax, self.ymax, self.ymin])

    @property
    def lmax(self):
        return self.__lmax


def distance_between_two_squares(r, s):
    dx = min([abs(r.xmin - s.xmin), abs(r.xmin - s.xmax),
              abs(r.xmax - s.xmin), abs(r.xmax - s.xmax)])
    dy = min([abs(r.ymin - s.ymin), abs(r.ymin - s.ymax),
              abs(r.ymax - s.ymin), abs(r.ymax - s.ymax)])
    return sqrt(dx*dx + dy*dy)


class split_tree:
    def __init__(self, S):
        self.s = copy(S)
        self.__root = _node(self, 0, len(self.s))

    def wspd(self, s):
        assert(s > 0)
        stack = [(v.left, v.right) for v in self if not v.is_leaf()]
        while stack:
            v, w = stack.pop()
            if self.__is_well_separated(v, w, s):
                yield (v, w)
            else:
                if v.rect_size < w.rect_size:
                    stack += [(v, w.left), (v, w.right)]
                else:
                    stack += [(v.left, w), (v.right, w)]

    @staticmethod
    def __is_well_separated(a, b, s):
        if a is None or b is None or len(a) == 0 or len(b) == 0:
            return False
        ca, cb = msw(list(a)), msw(list(b))     # smallest enclosing circle
        (ax, ay), (bx, by) = ca.center, cb.center
        radius = max(ca.radius, cb.radius)
        return ((ax-bx)**2 + (ay-by)**2)**0.5 - 2 * radius > s * radius

    def __iter__(self):
        stack = [self.__root]
        while stack:
            v = stack.pop()
            yield v
            if not v.is_leaf():
                if v.right:
                    stack.append(v.right)
                if v.left:
                    stack.append(v.left)


class _node:
    def __init__(self, tree, s, t):
        self.__tree = tree
        self.__start, self.__stop = s, t
        self.__r, self.left, self.right = None, None, None

        if abs(s - t) < 2:
            return
        self.__r = bounding_rectangle(tree.s[s:t])
        i = self.__split()
        self.left = _node(self.__tree, s, i) if s < i else None
        self.right = _node(self.__tree, i, t) if i < t else None

    def __split(self):
        left, right = self.__start, self.__stop-1
        lst = self.__tree.s
        axis, pivot = self.__r.axis()
        while left < right:
            while lst[left][axis] < pivot:
                left += 1
            while lst[right][axis] > pivot:
                right -= 1
            if left < right:
                lst[left], lst[right] = lst[right], lst[left]
        return left

    def __iter__(self):
        yield from self.__tree.s[self.__start:self.__stop]

    def draw(self, ax=None):
        if self.__r is not None:
            self.__r.draw(ax=ax)

    def is_leaf(self):
        return abs(self.__start - self.__stop) < 2

    def __repr__(self):
        pts, s, t = self.__tree.s, self.__start, self.__stop
        return f'start: {s}, stop: {t}, {pts[s:t]}'

    @property
    def rect_size(self):
        return self.__r.lmax if self.__r is not None else 0.

    def __len__(self):
        return self.__stop - self.__start


def gen(n=30, s=0):
    seed(s)
    return [(random(), random()) for i in range(n)]


def test_separated_exactly(pts, s):
    wspd = list(split_tree(pts).wspd(s))
    return all(sum(1 for a, b in wspd if (p in list(a) and q in list(b) or
                                          p in list(b) and q in list(a))) == 1
               for p, q in combinations(pts, 2))


if __name__ == '__main__':
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    S = gen()
    # ax1.scatter([x for x, _ in S], [y for _, y in S], zorder=10)
    print(test_separated_exactly(S, 1))

    t = split_tree(S)
    # for v in t:
    #    v.draw(ax=ax1)
    # ax1.set_title('Split tree')

    ax2 = plt.gca()
    s = 1
    for i, (a, b) in enumerate(t.wspd(s)):
        ax2.cla()
        la, lb = list(a), list(b)

        ax2.set_title(f'Well-separated pair decomposition with s = {s}')
        ax2.scatter([x for x, _ in la], [y for _, y in la], c='r')
        ax2.scatter([x for x, _ in lb], [y for _, y in lb], c='b')
        msw(la).draw(ax=ax2)
        msw(lb).draw(ax=ax2)

        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.set_aspect('equal')
        plt.draw()
        # plt.savefig(f'wspd_{str(i).zfill(2)}.png', bbox_inches='tight')
        plt.pause(0.5)

#    plt.gca().set_xlim(0, 1)
#    plt.gca().set_ylim(0, 1)
#    plt.gca().set_aspect('equal')
#    plt.tight_layout()
    # plt.savefig('split_tree_ex.png', bbox_inches='tight')
    plt.show()
