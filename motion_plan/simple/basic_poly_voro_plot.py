import cPickle as pickle
import math
import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
from scipy.spatial import Voronoi


class poly_voro:
    def __init__(self, poly):
        self.poly = poly
        self.ridges = []
        self.__preproc()

    def __extract_obstacles(self):
        facets = []
        if self.poly.type == 'Polygon':
            v = [list(p) for p in self.poly.exterior.coords[:]]
            facets.append([list(s) for s in zip(v[:-1], v[1:])])
            for i in self.poly.interiors:
                v = [list(p) for p in i.coords[:]]
                facets.append([list(s) for s in zip(v[:-1], v[1:])])
        else:
            raise ValueError('Unhandled type: ' + repr(self.poly.type))
        return facets

    def __is_ridge(self, p, q):
        return self.poly.contains(p) and self.poly.contains(q)

    def __preproc(self):
        sites = []
        for lol in self.__extract_obstacles():
            sites += self.__subdivide(lol)
        vor = Voronoi(sites)
        V = vor.vertices
        for i, ridge in enumerate(vor.ridge_vertices):
            if -1 in ridge:
                continue
            p, q = V[ridge[0]], V[ridge[1]]
            if self.__is_ridge(Point(p), Point(q)):
                self.ridges.append([p.tolist(), q.tolist()])

    def draw(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='box')
        patch = PolygonPatch(self.poly, facecolor='#6699cc', linewidth=2)
        ax.add_patch(patch)
        ax.add_collection(mc.LineCollection(self.ridges, linewidths=1))
        ax.autoscale()
        ax.margins(0.1)
        plt.show()

    def savefig(self, fname):
        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='box')
        patch = PolygonPatch(self.poly, facecolor='#6699cc', linewidth=2)
        ax.add_patch(patch)
        ax.add_collection(mc.LineCollection(self.ridges, linewidths=1))
        ax.autoscale()
        ax.margins(0.1)
        plt.savefig(fname, bbox_inches='tight')
        plt.close()

    def __length(self, l):
        x0, y0 = l[0]
        x1, y1 = l[1]
        return math.sqrt((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1))

    def __subdivide(self, list_of_lines):
        sub_points = []
        for l in list_of_lines:
            n = self.__length(l) / 0.2
            dx = (l[1][0] - l[0][0]) / n
            dy = (l[1][1] - l[0][1]) / n
            sub_points += [l[0]]
            for i in range(1, int(n)):
                sub_points.append([l[0][0] + dx * i, l[0][1] + dy * i])
        return sub_points


if __name__ == '__main__':
    if not os.path.exists('basic_01.dat'):
        subprocess.call('python ./basic_floor_sketch.py', shell=True)
    with open('basic_01.dat', 'r') as f:
        o = pickle.load(f)
    floor_sketch = cascaded_union([Polygon(p) for p in o])
    pv = poly_voro(floor_sketch)
    pv.draw()
