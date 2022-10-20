from itertools import product
from matplotlib import pyplot as plt


class bowyer_watson:
    def __init__(self, pts):
        self._v = [vertex(x, y) for x, y in pts]
        self._t = self.__triangulate()

    def __triangulate(self):
        t = [st := triangle([vertex(-9, -9), vertex(9, -9), vertex(0, 9)])]
        for v in self._v:
            t = self.__add(v, t)
        return [ti for ti in t if ti.is_valid_for(st)]

    def __add(self, v, triangles):
        new_t, edges = [], []
        for t in triangles:
            if not t.contains(v.x, v.y):
                new_t.append(t)
                continue
            for e in t.edges:
                if e in edges:
                    edges.remove(e)
                else:
                    edges.append(e)
        return new_t + [triangle([e.u, e.v, v]) for e in edges]

    def draw(self):
        for t in self._t:
            t.draw()


class triangle:
    def __init__(self, vertices):
        assert(len(vertices) == 3)
        self.__v = vertices if self.__ccw(vertices) else vertices[::-1]
        self.__e = [edge(self.__v[i], self.__v[(i+1) % 3]) for i in range(3)]

    @staticmethod
    def __ccw(v):
        px, py, qx, qy, rx, ry = v[0].x, v[0].y, v[1].x, v[1].y, v[2].x, v[2].y
        return ((qx - px) * (ry - py) - (qy - py) * (rx - px)) < 0

    def __iter__(self):
        yield from self.__v

    @property
    def edges(self):
        return self.__e

    def contains(self, x, y):
        v = self.__v
        ax, ay, bx, by, cx, cy = v[0].x, v[0].y, v[1].x, v[1].y, v[2].x, v[2].y
        x_ad, y_ad, x_bd, y_bd, x_cd, y_cd = ax-x, ay-y, bx-x, by-y, cx-x, cy-y
        sa, sb, sc, sd = ax**2+ay**2, bx**2+by**2, cx**2+cy**2, x**2+y**2
        s1, s2, s3 = sa-sd, sb-sd, sc-sd
        det = (x_ad * y_bd * s3) + (x_bd * y_cd * s1) + (x_cd * y_ad * s2)
        det -= (s1 * y_bd * x_cd) + (s2 * y_cd * x_ad) + (s3 * y_ad * x_bd)
        return det < 0

    def is_valid_for(self, st):
        return all(v != st_v for v, st_v in product(self, st))

    def draw(self):
        for v in self.__v:
            v.draw()
        for e in self.__e:
            e.draw()


class edge:
    def __init__(self, u, v):
        self.u, self.v = u, v

    def __eq__(self, other):
        return ((self.u == other.u and self.v == other.v) or
                (self.u == other.v and self.v == other.u))

    def draw(self):
        plt.plot([self.u.x, self.v.x], [self.u.y, self.v.y], zorder=5)


class vertex:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def draw(self):
        plt.scatter([self.x], [self.y], zorder=10)


if __name__ == '__main__':
    from random import random, seed
    seed(0)
    pts = [(random(), random()) for i in range(100)]
    dt = bowyer_watson(pts)
    dt.draw()

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.show()
