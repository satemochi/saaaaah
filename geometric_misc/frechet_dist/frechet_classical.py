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

    @cached_property
    def length(self):   # length of self (measured by Euclidean)
        return sum(dist(p, q) for p, q in zip(self.__pts, self.__pts[1:]))

    def frechet_dist(self, other, eps=0.01):
        """ ref) CGAL Frechet_classical.h

            TODO: init _max is not confortable
                    (diagonal length of union of bbox is better?) """
        _min, _max = 0, self.length + other.length
        while _max - _min >= eps:
            split = (_max + _min) / 2
            if self.__less_than(other, split):
                _max = split
            else:
                _min = split
        return (_min, _max)

    def __less_than(self, other, d):
        """ ref) On configuration space / free diagram
                https://sarielhp.org/book/ (good note by Sariel Har-Peled)
            [paper] Alt and Godau (1995)
                Computing the Frechet distance between two polygonal curves

            TODO: containing redundant sentences (need more if-else states)
        """
        square_dist = d * d
        if (self.__square_dist(self[0], other[0]) > square_dist or
                self.__square_dist(self[-1], other[-1]) > square_dist):
            return False
        checked, stack = set(), [(0, 0)]
        while stack:
            i, j = stack.pop()
            checked.add((i, j))
            if (i, j) == (self.n_cell, other.n_cell):
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
