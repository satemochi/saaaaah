import cPickle as pickle
import itertools
import math
import os
import subprocess
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
import visilibity as vis


def find_leftmost(V):
    return min(enumerate(V), key=lambda x: x[1])[0]


def check_triple(V, i):
    a, b, c = V[i % len(V)], V[(i + 1) % len(V)], V[(i + 2) % len(V)]
    if (a[0] == b[0] and b[0] == c[0]) or (a[1] == b[1] and b[1] == c[1]):
        return True
    return False


def simplify(V):
    o = find_leftmost(V)
    E = []
    i = o
    while True:
        if (i + 1) % len(V) == o:
            break
        if check_triple(V, i):
            E.append((i + 1) % len(V))
        i += 1
    for i in sorted(E)[::-1]:
        del V[i]
    return V


def poly_list(poly):
    V = []
    if poly.type == 'Polygon':
        V.append(simplify([list(p) for p in poly.exterior.coords[:-1]])[::-1])
        for i in poly.interiors:
            V.append(simplify([list(p) for p in i.coords[:-1]])[::-1])
    return V


def vis_graph(poly):
    P = poly_list(poly)
    vis_polygons = []
    for p in P:
        vis_polygons.append(vis.Polygon([vis.Point(x, y) for x, y in p]))
    env = vis.Environment(vis_polygons)
    vg = vis.Visibility_Graph(env, 0.000001)
    edges = []
    for i, j in itertools.combinations(range(vg.n()), 2):
        if vg(i, j):
            edges.append([[env(i).x(), env(i).y()], [env(j).x(), env(j).y()]])
    plt.gca().add_collection(mc.LineCollection(edges, color='g'))
    print len(edges)


def draw(poly):
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().add_patch(PolygonPatch(poly, facecolor='#6699cc', linewidth=2))
    vis_graph(poly)


if __name__ == '__main__':
    if not os.path.exists('basic_01.dat'):
        subprocess.call('python ./basic_floor_sketch.py', shell=True)
    with open('basic_01.dat', 'r') as f:
        o = pickle.load(f)
    floor_sketch = cascaded_union([Polygon(p) for p in o])
    draw(floor_sketch)

    plt.gca().autoscale()
    plt.gca().margins(0.1)
    plt.show()
