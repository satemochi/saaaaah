import cPickle as pickle
import itertools
import os
from glob import glob
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import networkx as nx
import numpy as np
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from scipy.spatial import Voronoi
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


def get_st(env):
    s, t = 0, 0
    for i in range(0, env.n()):
        if env(s).x() > env(i).x():
            s = i
        elif env(s).x() == env(i).x() and env(s).y() > env(i).y():
            s = i
        if env(t).x() < env(i).x():
            t = i
        elif env(t).x() == env(i).x() and env(t).y() < env(i).y():
            t = i
    return (s, t)


def vis_graph(poly):
    P = poly_list(poly)
    vis_polygons = []
    for p in P:
        vis_polygons.append(vis.Polygon([vis.Point(x, y) for x, y in p]))
    env = vis.Environment(vis_polygons)
    vg = vis.Visibility_Graph(env, 0.000001)

    edges = []
    G = nx.Graph()
    for i, j in itertools.combinations(range(vg.n()), 2):
        if vg(i, j):
            edges.append([[env(i).x(), env(i).y()], [env(j).x(), env(j).y()]])
            G.add_edge(i, j, weight=np.linalg.norm(np.array(edges[-1][0]) -
                                                   np.array(edges[-1][1])))
    plt.gca().add_collection(mc.LineCollection(edges, color='g'))

    s, t = get_st(env)
    sp = [i for i in nx.shortest_path(G, s, t, 'weight')]
    sp_edges = [[[env(i).x(), env(i).y()], [env(j).x(), env(j).y()]]
                for i, j in zip(sp[:-1], sp[1:])]
    plt.gca().add_collection(mc.LineCollection(sp_edges, color='r', lw=2))


def draw(poly):
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().add_patch(PolygonPatch(poly, facecolor='#6699cc', linewidth=2))
    vis_graph(poly)


def savefig(poly, fname):
    draw(poly)
    plt.gca().autoscale()
    plt.gca().margins(0.1)
    plt.savefig(fname, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    out_dir = 'vg_img/'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    for d in glob('dat/*.dat'):
        fname = out_dir + d[4:-4] + '-vg.png'
        print fname
        if os.path.exists(fname):
            continue
        with open(d, 'r') as f:
            o = pickle.load(f)
        floor_sketch = cascaded_union([Polygon(p) for p in o])
        savefig(floor_sketch.simplify(0.0001, preserve_topology=False), fname)
