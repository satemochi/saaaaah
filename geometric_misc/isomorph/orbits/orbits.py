from itertools import combinations
import matplotlib
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
from knuth_u import algorithm_u


def gen():
    g = nx.Graph([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 3), (2, 4)])
    pos = {v: (np.cos(pi), np.sin(pi))
           for v, pi in enumerate(np.linspace(0, 2*np.pi, 6))}
    return g, pos


def all_partitions(g, s):
    for i in range(1, len(s)):
        for ss in algorithm_u(s, i):
            yield ss


def is_same_degree(g, u, v):
    return g.degree(u) == g.degree(v)


def is_same_neighbors(g, u, v):
    return set(g[u]) - set([v]) == set(g[v]) - set([u])


def is_vorbit_pair(g, u, v):
    return is_same_degree(g, u, v) and is_same_neighbors(g, u, v)


def is_vorbit_group(g, s):
    if len(s) == 1:
        return True
    return all(is_vorbit_pair(g, u, v) for u, v in combinations(s, 2))


def vertex_orbits(g):
    for ss in all_partitions(g, list(g.nodes())):
        if all(is_vorbit_group(g, s) for s in ss):
            return ss


def deg_pair(g, x, y):
    d1, d2 = g.degree(x), g.degree(y)
    return (d1, d2) if d1 < d2 else (d2, d1)


def is_same_degrees(g, e, f):
    return deg_pair(g, *e) == deg_pair(g, *f)


def is_same_endpoints_neighbors(g, e, f):
    (u, v), (x, y) = e, f
    return (is_same_neighbors(g, u, x) and is_same_neighbors(g, v, y) or
            is_same_neighbors(g, v, x) and is_same_neighbors(g, u, y))


def is_eorbit_pair(g, e, f):
    return is_same_degrees(g, e, f) and is_same_endpoints_neighbors(g, e, f)


def is_eorbit_group(g, s):
    if len(s) == 1:
        return True
    return all(is_eorbit_pair(g, e, f) for e, f in combinations(s, 2))


def edge_orbits(g):
    for ss in all_partitions(g, list(g.edges())):
        if all(is_eorbit_group(g, s) for s in ss):
            return ss


if __name__ == '__main__':
    g, pos = gen()
    print(vertex_orbits(g))
    print(edge_orbits(g))

#    matplotlib.use('module://backend_ipe')
#    isy = "/Applications/Ipe.app/Contents/Resources/styles/basic.isy"
#    matplotlib.rcParams['ipe.stylesheet'] = isy
    nx.draw_networkx(g, pos, node_color='#ff9999')
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.show()
#    plt.savefig('orbits_01.ipe', format='ipe')
