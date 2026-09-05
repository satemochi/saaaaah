from functools import wraps
from math import cos, pi, sin
from unittest import TestCase, main

from matplotlib import pyplot as plt, use
import networkx as nx
from pulp import LpProblem, lpSum, LpVariable, PULP_CBC_CMD


def _raise_on_directed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        create_using = args[0] if args else kwargs.get("create_using")
        if create_using is not None:
            G = nx.empty_graph(create_using=create_using)
            if G.is_directed():
                raise nx.NetworkXError("Directed Graph not supported in create_using")
        return func(*args, **kwargs)

    return wrapper


@_raise_on_directed
@nx._dispatchable(graphs=None, returns_graph=True)
def shrikhande_graph(create_using=None):
    rows = cols = range(4)
    plus_one = [1, 2, 3, 0]
    G = nx.empty_graph(0, create_using=create_using)
    G.name = "Shrikhande Graph"
    G.add_edges_from(((x, y), (plus_one[x], y)) for x in rows for y in cols)
    G.add_edges_from(((x, y), (x, plus_one[y])) for x in rows for y in cols)
    G.add_edges_from(((x, y), (plus_one[x], plus_one[y])) for x in rows for y in cols)
    return G

def __shrikhande_graph():
    from itertools import product
    _ = {(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1)}
    g = nx.Graph(((u, v), ((u+w) % 4, (v+x) % 4))
                 for (u, v), (w, x) in product(product(range(4), range(4)), _))
    return g


def duo_octagons_layout():
    inner = [(0, 0), (3, 2), (1, 1), (0, 3), (2, 2), (1, 0), (3, 3), (2, 1)]
    outer = [(3, 1), (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 0), (3, 0)]
    t, w = 2*pi / 8, 2*pi / 16
    pos = {v: (cos(t*i-w), sin(t*i-w)) for i, v in enumerate(inner)}
    pos |= {v: (2.5*cos(t*i-w), 2.5*sin(t*i-w)) for i, v in enumerate(outer)}
    return pos


def quintet_squares_layout():
    s1 = [(0, 3), (3, 2), (2, 1), (1, 0)]
    s2 = [(1, 1), (1, 3), (3, 3), (3, 1)]
    s3 = [(0, 2), (2, 2), (2, 0), (0, 0)]
    s4 = [(0, 1), (1, 2), (2, 3), (3, 0)]
    t, w = 2*pi / 4, 2*pi / 8
    pos = {v: (2.5*cos(t*i-w), 2.5*sin(t*i-w)) for i, v in enumerate(s1)}
    pos |= {v: (4.0*cos(t*i), 4.0*sin(t*i)) for i, v in enumerate(s2)}
    pos |= {v: (5.5*cos(t*i), 5.5*sin(t*i)) for i, v in enumerate(s3)}
    pos |= {v: (8.5*cos(t*i-w), 8.5*sin(t*i-w)) for i, v in enumerate(s4)}
    return pos


def assign(g, h=10):   # Graph Coloring ILP (by assignment approch)
    c = list(range(h))
    w = [LpVariable(f'w{j}', cat='Binary') for j in c]
    x = {i: [LpVariable(f'x{i},{j}', cat='Binary') for j in c] for i in g}
    lp = LpProblem()
    lp += lpSum(w)
    for i in g:
        lp += lpSum(x[i]) == 1
    for u, v in g.edges:
        for j in c:
            lp += x[u][j] + x[v][j] <= w[j]
    for j in c:
        lp += w[j] <= lpSum([x[i][j] for i in g])
    for j in c[1:]:
        lp += w[j] <= w[j-1]
    PULP_CBC_CMD(msg=0).solve(lp)
    return [[xi.varValue for xi in x[i]].index(1.0) for i in g]


class test_dual_numbers(TestCase):
    def test_adjacency(self):
        g = shrikhande_graph()
        _ = {(1, 0), (0, 1), (1, 1), (3, 0), (0, 3), (3, 3)}    # -1 % 4 = 3
        for (a, b), (c, d) in g.edges:
            self.assertTrue(((a - c) % 4, (b - d) % 4) in _)

    def test_property(self):
        g = shrikhande_graph()
        self.assertTrue(sorted(g) == [(u, v) for u in range(4)
                                      for v in range(4)])
        self.assertTrue(g.number_of_edges() == 48)
        self.assertTrue([d for n, d in g.degree()] == 16 * [6])


if __name__ == '__main__':
    g = shrikhande_graph()

    cmap = plt.get_cmap('tab10')
    colors = [cmap(c) for c in assign(g)]
    positions = [duo_octagons_layout(), quintet_squares_layout()]

#    use('module://backend_ipe')
    _, axes = plt.subplots(1, 2, figsize=(10, 5))
    for pos, ax in zip(positions, axes):
        nx.draw_networkx_nodes(g, pos, ax=ax, node_size=500,
                               node_color=colors).set_edgecolor('k')
        nx.draw_networkx_edges(g, pos, ax=ax)
        nx.draw_networkx_labels(g, pos, ax=ax, font_size=7)
        ax.set_aspect('equal')
        ax.axis('off')

    plt.tight_layout()
    # plt.savefig('shrikhande.ipe')
    # plt.savefig('shrikhande.png')
    plt.show()

    main()
