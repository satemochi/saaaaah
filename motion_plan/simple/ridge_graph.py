from poly_voro import poly_voro
import cPickle as pickle
from itertools import combinations
import math
import os
import subprocess
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.collections as mc


class ridge_graph:
    def __init__(self, ridges):
        self.__ridges = ridges
        self.__g = self.__const_graph()

    def __const_graph(self):
        edges = []
        for s, t in combinations(range(len(self.__ridges)), 2):
            if self.__is_connected(s, t):
                edges.append((s, t, self.__length(s) + self.__length(t)))
        g = nx.Graph()
        g.add_weighted_edges_from(edges)
        return g

    def __is_connected(self, i, j):
        si = self.__ridges[i][0]
        ti = self.__ridges[i][1]
        sj = self.__ridges[j][0]
        tj = self.__ridges[j][1]
        return True if si == sj or si == tj or ti == sj or ti == tj else False

    def __length(self, i):
        sx, sy = self.__ridges[i][0]
        tx, ty = self.__ridges[i][1]
        return math.sqrt((sx-tx)**2 + (sy-ty)**2)

    def get_sp_ridges(self, s, t):
        return [self.__ridges[i]
                for i in nx.shortest_path(self.__g, s, t, 'weight')]


def get_st(ridges):
    bl, tr = 0, 0
    for i in range(1, len(ridges)):
        if ridges[bl][0] > ridges[i][0]:
            bl = i
        elif ridges[bl][0] == ridges[i][0] and ridges[bl][1] > ridges[i][1]:
            bl = i
        if ridges[tr][0] < ridges[i][0]:
            tr = i
        elif ridges[tr][0] == ridges[i][0] and ridges[tr][1] < ridges[i][1]:
            tr = i
    return (bl, tr)


if __name__ == '__main__':
    if not os.path.exists('dat/003.dat'):
        subprocess.call('python ./gen_at_most_30_floor_sketches_from_sp.py',
                        shell=True)
    with open('dat/003.dat', 'r') as f:
        o = pickle.load(f)
    floor_sketch = cascaded_union([Polygon(p) for p in o])
    pv = poly_voro(floor_sketch)
    rg = ridge_graph(pv.ridges)
    s, t = get_st(pv.ridges)
    sp_ridges = rg.get_sp_ridges(s, t)

    fig, ax = plt.subplots()
    patch = PolygonPatch(floor_sketch, facecolor='#6699cc', linewidth=2)
    ax.add_patch(patch)
    ax.add_collection(mc.LineCollection(pv.ridges))
    ax.add_collection(mc.LineCollection(sp_ridges, colors='r', linewidth=2))
    ax.autoscale()
    ax.margins(0.1)
    plt.show()
