from functools import cached_property
from math import isclose, sqrt
from matplotlib import pyplot as plt
import numpy as np


class pc:   # polygonal curve
    def __init__(self, pts):
        self.__pts = pts

    def draw(self, ax=None):
        if ax is None:
            ax = plt.gca()
        ax.plot([x for x, _ in self.__pts], [y for _, y in self.__pts])

    def __getitem__(self, key):
        return self.__pts[key]

    def __repr__(self):
        return f"{', '.join([f'({x:.2f}, {y:.2f})' for x, y in self.__pts])}"

    @cached_property
    def n_ind(self):    # number of indices
        return len(self.__pts) - 1

    @cached_property
    def n_cell(self):   # number of cells for self
        return len(self.__pts) - 2

    def get_p(self, i):
        assert (i <= self.n_ind)
        if i == self.n_ind:
            return self.__pts[-1]
        _i, _a = int(i), i - int(i)
        (xi, yi), (xii, yii) = self.__pts[_i], self.__pts[_i+1]
        return (xi + (xii-xi)*_a, yi + (yii - yi)*_a)

    def free_space(self, other, eps=0.450, acc=500):
        x = np.linspace(0, self.n_ind, acc)
        y = np.linspace(0, other.n_ind, acc)
        c = []
        s_eps = eps * eps
        for yi in y:
            qi = other.get_p(yi)
            ci = []
            for xi in x:
                pi = self.get_p(xi)
                _ = 0 if (pi[0]-qi[0])**2+(pi[1]-qi[1])**2 < s_eps else 1
                ci.append(_)
            c.append(ci)
        return x, y, c

    @staticmethod
    def __square_dist(p, q):
        return sum((pi - qi)**2 for pi, qi in zip(p, q))

    def less_than(self, other, dist):
        square_dist = dist * dist
        if (self.__square_dist(self[0], other[0]) > square_dist or
                self.__square_dist(self[-1], other[-1]) > square_dist):
            return False
        checked, stack = set(), [(0, 0)]
        while stack:
            i, j = stack.pop()
            checked.add((i, j))
            if (i, j) == (self.n_cell, other.n_cell):
                return True
            if (frac := self.__int(self[i+1], other[j], other[j+1], dist)):
                plt.gca().plot([i+1, i+1], [j+ti for ti in frac], c='g')
                if (i+1, j) not in checked and i+1 < self.n_ind:
                    stack.append((i+1, j))
            if (frac := self.__int(other[j+1], self[i], self[i+1], dist)):
                plt.gca().plot([i+ti for ti in frac], [j+1, j+1], c='g')
                if (i, j+1) not in checked and j+1 < other.n_ind:
                    stack.append((i, j+1))
        return False

    @staticmethod
    def __int(c, pt1, pt2, r):
        """ ref) http://mathworld.wolfram.com/Circle-LineIntersection.html """
        (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, c
        (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
        dx, dy = (x2 - x1), (y2 - y1)
        dr, d = dx * dx + dy * dy, x1 * y2 - x2 * y1
        if (discriminant := (r * r) * dr - (d * d)) < 0:
            return False
        sqrt_d = sqrt(discriminant)

        i = [(cx + (d * dy + sign * (-1 if dy < 0 else 1) * dx * sqrt_d) / dr,
              cy + (-d * dx + sign * abs(dy) * sqrt_d) / dr)
             for sign in ((1, -1) if dy < 0 else (-1, 1))]
        frac = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy

                for xi, yi in i]

        if len(frac) == 2:
            if frac[0] > 1 or frac[1] < 0:
                return False
            if not isclose(discriminant, 0):
                return [max(frac[0], 0), min(frac[1], 1)]
            frac = [frac[0]]
        if 0 <= frac[0] <= 1:
            return frac
        return False


def gen(n=10, m=12):
    p = pc([((i+1)/n, np.random.rand()) for i in range(n)])
    q = pc([((i+1)/m, np.random.rand()) for i in range(m)])
    return p, q


if __name__ == '__main__':
    np.random.seed(9)
    p, q = gen()

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    p.draw(ax1)
    q.draw(ax1)
    dist = 0.5

    if p.less_than(q, dist):
        print(f'frechet distance is less than {dist}')
    else:
        print(f'false within {dist}')

    x, y, c = p.free_space(q, eps=dist)
    ax2.pcolormesh(x, y, c, vmin=np.min(c), vmax=np.max(c),
                   shading='auto', cmap=plt.colormaps['Wistia'])

    ax1.set_aspect('equal')
    ax2.set_title(f'epsilon = {dist}')
    ax2.set_aspect('equal')
    plt.savefig('frechet2.png', bbox_inches='tight')
    plt.tight_layout()
    plt.show()
