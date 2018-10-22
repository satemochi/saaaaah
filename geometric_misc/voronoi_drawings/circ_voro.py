from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import numpy as np
from scipy.spatial import Voronoi


class circle:
    def __init__(self, ((x, y), r)):
        self.x, self.y, self.r = x, y, r
        self.points = self.__split()

    def __split(self):
        t = np.linspace(0, 2 * np.pi, num=64)
        dx, dy = self.x + self.r * np.cos(t), self.y + self.r * np.sin(t)
        return [[x, y] for x, y in zip(dx, dy)]

    def opposite(self, p, q):
        judge1 = (p in self.points) and (q not in self.points)
        judge2 = (p not in self.points) and (q in self.points)
        return judge1 or judge2

    def draw(self):
        plt.gca().add_patch(plt.Circle((self.x, self.y), self.r, fill=False))


class circ_voro:
    def __init__(self, C):
        self.circs = [circle(c) for c in C]
        self.sites = list(chain.from_iterable([c.points for c in self.circs]))
        self.ridges = []
        self.__preproc()

    def __is_ridge(self, p, q):
        for c in self.circs:
            if c.opposite(p.tolist(), q.tolist()) is True:
                return True
        return False

    def __preproc(self):
        vor = Voronoi(self.sites)
        V = vor.vertices
        for j, ridge in enumerate(vor.ridge_vertices):
            if -1 not in ridge:
                p, q = vor.ridge_points[j]
                if self.__is_ridge(vor.points[p], vor.points[q]):
                    self.ridges.append([(V[ridge[0]][0], V[ridge[0]][1]),
                                        (V[ridge[1]][0], V[ridge[1]][1])])

    def draw(self):
        for c in self.circs:
            c.draw()
        lc = mc.LineCollection(self.ridges, linewidths=1)
        plt.gca().add_collection(lc)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.gca().set_xlim(0, 1)
        plt.gca().set_ylim(0, 1)
        plt.show()


def random_circles(n=30):
    centers = np.random.random((n, 2))
    radii = np.random.uniform(0, 0.1, n)
    circles = zip(centers.tolist(), radii)
    return circles


if __name__ == '__main__':
    cv = circ_voro(random_circles())
    cv.draw()
