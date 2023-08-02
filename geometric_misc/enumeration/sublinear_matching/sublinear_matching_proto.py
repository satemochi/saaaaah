from bisect import bisect_left
from functools import reduce
from math import log
from random import choice, shuffle, uniform
from matplotlib import pyplot as plt
import networkx as nx


def get_matching(g, n, m, md, degs, eps=0.2):
    p, k, a, c, j_aster, frozen = __setup(n, md, eps)
    t = __construct_t(g, k)
    m, s = nx.Graph(), nx.Graph()
    m_ = [nx.Graph() for _ in range(len(a)-1)]
    for i, ((u, v), x) in enumerate(t):
        if x == 'start' and (not m.has_node(u)) and (not m.has_node(v)):
            m.add_edge(u, v)
            m_[bisect_left(a, i/len(t))].add_edge(u, v)
            if c[u] == c[v] or not m_[j_aster].has_edge(u, v):
                frozen.union((u, v))
            elif uniform(0, 1) < 1 - p:
                frozen.union((u, v))
        if (x == 'extend' and (not s.has_node(u) and not s.has_node(v)) and
                (m.has_node(u) and m.has_node(v) and
                 m.degree(u) + m.degree(v) <= 1 and c[u] != c[v]) and
                (u not in frozen and v not in frozen)):
            s.add_edge(u, v)
    return set(m.edges) | set(s.edges)


def __setup(n, md, eps):
    p, d = 0.007, (0.001 * md * log(n))**eps
    k = int(10*d*(log(n))**2)
    a = [0] + reduce(lambda x, i: [x[0]/d]+x, range(int(2/eps)), [1])
    return (p, k, a, {v: choice(('blue', 'red')) for v in g},
            choice(range(len(a)-1)), set())


def __construct_t(g, k):
    shuffle(t := reduce(lambda a, e: a + [(e, 'extend')] +
                        [(e, 'start') for _ in range(k)], g.edges(), []))
    return t


def gen():
    g = nx.frucht_graph()
    n, m, degs = g.order(), g.size(), dict(g.degree)
    return g, n, m, max(_ for _ in degs.values()), degs


if __name__ == '__main__':
    g, n, m, md, degs = gen()
    mat = get_matching(g, n, m, md, degs)
    print(mat)
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color='#ffcccc').set_edgecolor('k')
    nx.draw_networkx_edges(g, pos, alpha=0.3)
    nx.draw_networkx_edges(g, pos, edgelist=mat, edge_color='r')
    nx.draw_networkx_labels(g, pos)
    plt.gca().set_aspect('equal')
    plt.gca().axis('off')
    plt.tight_layout()
#    plt.savefig('sublinear_matching_proto.png', bbox_inches='tight')
    plt.show()
