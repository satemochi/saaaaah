from itertools import combinations
from math import sqrt
from random import random, seed, shuffle
from matplotlib import pyplot as plt


class circle:
    def __init__(self, pts, idx):
        self.__pts = tuple(pts[i] for i in idx)
        if len(idx) == 2:
            self.__c, self.__r = self.__c2()
        else:
            self.__c, self.__r = self.__c3()
        self.__sr = self.__r * self.__r

    def __c2(self):
        (x0, y0), (x1, y1) = self.__pts
        return ((0.5*(x0+x1), 0.5*(y0+y1)),
                0.5*sqrt((x0-x1)*(x0-x1) + (y0-y1)*(y0-y1)))

    def __c3(self):
        return self.__o3() if self.__obtuse() else self.__a3()

    def __o3(self):
        p, q = max(((xi-xj)**2 + (yi-yj)**2, ((xi, yi), (xj, yj)))
                   for (xi, yi), (xj, yj) in combinations(self.__pts, 2))[1]
        self.__pts = [p, q]
        return self.__c2()

    def __obtuse(self):
        (x0, y0), (x1, y1), (x2, y2) = self.__pts
        a = (x0-x1)*(x0-x1) + (y0-y1)*(y0-y1)
        b = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
        c = (x2-x0)*(x2-x0) + (y2-y0)*(y2-y0)
        return a > b+c or b > c+a or c > a+b

    def __a3(self):
        (x0, y0), (x1, y1), (x2, y2) = self.__pts

        x01, x02 = x0 - x1, x0 - x2
        y01, y02 = y0 - y1, y0 - y2

        y20, y10 = y2 - y0, y1 - y0
        x20, x10 = x2 - x0, x1 - x0

        sx02, sy02 = x0*x0 - x2*x2, y0*y0 - y2*y2
        sx10, sy10 = x1*x1 - x0*x0, y1*y1 - y0*y0

        f = (sx02*x01+sy02*x01 + sx10*x02+sy10*x02) / (2*(y20*x01 - y10*x02))
        g = (sx02*y01+sy02*y01 + sx10*y02+sy10*y02) / (2*(x20*y01 - x10*y02))
        c = -x0*x0 - y0*y0 - 2*g*x0 - 2*f*y0

        return ((-g, -f), sqrt(f*f + g*g - c))

    def contains(self, q):
        return (sum((xi - xj) * (xi - xj) for xi, xj in zip(self.__c, q))
                <= self.__sr + 1e-9)

    def draw(self):
        c = plt.Circle(self.__c, self.__r, fill=False, color='g')
        plt.gca().add_artist(c)


def sec(pts):
    shuffle((_pts := [p for p in pts]))
    c = circle(_pts, (0, 1))
    for i, q in enumerate(_pts[2:], start=2):
        if not c.contains(q):
            c = _sec1(_pts, i)
    return c


def _sec1(pts, i):
    c = circle(pts, (0, i))
    for j, q in enumerate(pts[1:i], start=1):
        if not c.contains(q):
            c = _sec2(pts, j, i)
    return c


def _sec2(pts, j, i):
    c = circle(pts, (j, i))
    for k, q in enumerate(pts[:i]):
        if not c.contains(q):
            c = circle(pts, (k, j, i))
    return c


def gen(n=20, s=1):
    seed(s)
    return [(random(), random()) for i in range(n)]


if __name__ == '__main__':
    sec(gen()).draw()

    plt.scatter([x for x, _ in pts], [y for _, y in pts])
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(-0.25, 1.25)
    plt.gca().set_ylim(-0.25, 1.25)
    plt.tight_layout()
    # plt.savefig('smallest_enclosing_circle.png', bbox_inches='tight')
    plt.show()
