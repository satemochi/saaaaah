from itertools import product
from matplotlib import pyplot as plt


class delaunay:
    """ good reference:
        Author: Gorilla Sun (Ahmad Moussa)
        Post:   Bowyer-Watson Algorithm for Delaunay Triangulation
        Link:
            https://gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation
    """
    def __init__(self, pts):
        self._v = [vertex(x, y) for x, y in pts]
        self._t = self.__triangulate()

    def __triangulate(self):
        triangles = [st := triangle([vertex(-10, -10), vertex(10, -10),
                                     vertex(0, 10)])]
        for v in self._v:
            triangles = self.__add(v, triangles)
        return [t for t in triangles if t.is_valid_for(st)]
        
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


class vertex:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def plot(self):
        plt.scatter([self.x], [self.y], zorder=10)
        

class edge:
    def __init__(self, u, v):
        self.u, self.v = u, v

    def __eq__(self, other):
        return ((self.u == other.u and self.v == other.v) or
                (self.u == other.v and self.v == other.u))

    def plot(self):
        plt.plot([self.u.x, self.v.x], [self.u.y, self.v.y], zorder=5)


class triangle:
    def __init__(self, vertices):
        assert(len(vertices) == 3)
        self.__v = vertices
        self.__e = [edge(self.__v[i], self.__v[(i+1)%3]) for i in range(3)]
        self.__cx, self.__cy, self.__r = self.__circumcircle()

    @property
    def edges(self):
        return self.__e

    def __circumcircle(self):
        """ Equation of circle when three points on the circle are given.
            https://www.geeksforgeeks.org/equation-of-circle-when-three-points-on-the-circle-are-given/
        """
        x0, y0 = self.__v[0].x, self.__v[0].y
        x1, y1 = self.__v[1].x, self.__v[1].y
        x2, y2 = self.__v[2].x, self.__v[2].y

        x01, x02 = x0 - x1, x0 - x2
        y01, y02 = y0 - y1, y0 - y2

        y20, y10 = y2 - y0, y1 - y0
        x20, x10 = x2 - x0, x1 - x0

        sx02, sy02 = x0*x0 - x2*x2, y0*y0 - y2*y2
        sx10, sy10 = x1*x1 - x0*x0, y1*y1 - y0*y0

        f = (sx02*x01+sy02*x01 + sx10*x02+sy10*x02) / (2*(y20*x01 - y10*x02))
        g = (sx02*y01+sy02*y01 + sx10*y02+sy10*y02) / (2*(x20*y01 - x10*y02))
        c = -x0*x0 - y0*y0 - 2*g*x0 - 2*f*y0

        return (-g, -f, (f*f + g*g - c)**0.5)

    def contains(self, x, y):
        return ((x-self.__cx)**2 + (y-self.__cy)**2)**0.5 <= self.__r + 1e-9

    def is_valid_for(self, st):
        return all(v != st_v for v, st_v in product(self, st))

    def __iter__(self):
        yield from self.__v

    def draw(self):
        for v in self.__v:
            v.plot()
        for e in self.__e:
            e.plot()


if __name__ == '__main__':
    from random import random, seed
    seed(0)
    pts = [(random(), random()) for i in range(100)]
    dt = delaunay(pts)
    dt.draw()

    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
    plt.savefig('delaunay_triang_with_bowyer_watson.png', bbox_inches='tight')
    plt.show()
