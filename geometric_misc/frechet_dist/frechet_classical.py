from functools import cached_property
from math import dist, isclose, sqrt


class pc:   # polygonal curve (static)
    def __init__(self, pts):
        self.__pts = pts

    def __getitem__(self, key):
        return self.__pts[key]

    @cached_property
    def n_ind(self):    # number of indices for configuration space
        return len(self.__pts) - 1

    @cached_property
    def n_cell(self):   # #-column in configuration; #-rows is other.n_cell.
        return len(self.__pts) - 2

    def frechet_dist(self, other, eps=1e-7):
        """ ref) CGAL Frechet_classical.h   """
        _min, _max = 0, self.__diag_len_of_bbox(self, other)
        while _max - _min >= eps:
            split = (_max + _min) / 2
            if self.__less_than(other, split):
                _max = split
            else:
                _min = split
        return (_min, _max)

    @staticmethod
    def __diag_len_of_bbox(*args):
        _l, _b = float('inf'), float('inf')
        _r, _a = -float('inf'), -float('inf')
        for pts in args:
            _l = min(_l, min(x for x, _ in pts))    # left
            _b = min(_b, min(y for _, y in pts))    # below
            _r = max(_r, max(x for x, _ in pts))    # right
            _a = max(_a, max(y for _, y in pts))    # above
        return dist((_l, _b), (_r, _a))

    def __less_than(self, other, d):
        """ ref) https://sarielhp.org/book/chapters/frechet.pdf
            TODO: containing redundant comp-paths (more if-else statements) """
        if (self.__square_dist(self[0], other[0]) > (dd := d * d) or
                self.__square_dist(self[-1], other[-1]) > dd):
            return False
        checked, stack = set(), [(0, 0)]
        while stack:
            i, j = stack.pop()
            checked.add((i, j))
            if (i, j) == (g := (self.n_cell, other.n_cell)):    # g: goal cell
                return True
            if self.__int(self[i+1], other[j], other[j+1], d):
                if (i+1, j) not in checked and i+1 < self.n_ind:
                    stack.append((i+1, j))
            if self.__int(other[j+1], self[i], self[i+1], d):
                if (i, j+1) not in checked and j+1 < other.n_ind:
                    stack.append((i, j+1))
        return False

    @staticmethod
    def __square_dist(p, q):
        return sum((pi - qi)**2 for pi, qi in zip(p, q))

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


if __name__ == '__main__':
    from random import random, seed
    seed(0)
    n, m = 10, 12
    p = pc([((i+1)/n, random()) for i in range(n)])
    q = pc([((i+1)/m, random()) for i in range(m)])
    print(p.frechet_dist(q))
