from collections import defaultdict
from pprint import pprint
from random import seed
from matplotlib import pyplot as plt
import networkx as nx


def suurballe(g, s=0, t=1):
    h = g.to_directed()
    lengths, paths = nx.single_source_dijkstra(h, s)
    for u, v in h.edges:
        g[u][v]['weight'] = 1 + lengths[u] - lengths[v]
    p1 = [e for e in zip(paths[t], paths[t][1:])]
    h.remove_edges_from(p1)
    p = nx.dijkstra_path(h, s, t)
    return _trim_duplicates(p1, [e for e in zip(p, p[1:])])


def _trim_duplicates(p1, p2):
    g = nx.DiGraph(p1 + p2)
    for u, v in p1:
        if g.has_edge(v, u):
            g.remove_edges_from([(u, v), (v, u)])
    q = nx.dijkstra_path(g, p1[0][0], p1[-1][-1])
    q1 = [e for e in zip(q, q[1:])]
    g.remove_edges_from(q1)
    q2 = nx.dijkstra_path(g, p1[0][0], p1[-1][-1])
    return q1, [e for e in zip(q2, q2[1:])]


def frechet(p, q):
    """
        T. Eiter, H. Mannila: (1994)
            Computing discrete Frechet distance
                CD-TR 94/64 Information Systems Department,
                Technical University of Vienna.
    """
    assert(len(p) == len(q))
    n = len(p)
    ca = defaultdict(lambda: -1)
    stack = [('dummy_ij', iter([(n-1, n-1)]))]
    while ca[n-1, n-1] < 0:
        try:
            i, j = next(stack[-1][1])
            if ca[i, j] >= 0:
                continue
            if i == 0 and j == 0:
                ca[i, j] = _norm(*p[i], *q[j])
            elif i > 0 and j == 0:
                stack.append(((i, j), iter([(i-1, 0)])))
            elif i == 0 and j > 0:
                stack.append(((i, j), iter([(0, j-1)])))
            elif i > 0 and j > 0:
                stack.append(((i, j), iter([(i-1, j), (i-1, j-1), (i, j-1)])))
            else:
                ca[i, j] = float('inf')
        except StopIteration:
            i, j = stack[-1][0]
            d = _norm(*p[i], *q[j])
            if i > 0 and j == 0:
                ca[i, j] = max(d, ca[i-1, 0])
            elif i == 0 and j > 0:
                ca[i, j] = max(d, ca[0, j-1])
            elif i > 0 and j > 0:
                ca[i, j] = max(d, min([ca[0, j-1], ca[i-1, j-1], ca[i-1, 0]]))
            stack.pop()
    return ca[n-1, n-1]


def _norm(a, b, c, d):
    return ((a - c)**2 + (b - d)**2)**0.5


def gen(n=300):
    seed(1)
    g = nx.random_geometric_graph(n, 0.15)
    return g, nx.get_node_attributes(g, 'pos')


if __name__ == '__main__':
    g, pos = gen()
    nx.draw(g, pos, alpha=0.15, node_size=35)

    p1, p2 = suurballe(g, s=10, t=6)

    nx.draw_networkx_edges(g, pos, edgelist=p1,
                           edge_color='r', width=1.5, alpha=0.7)
    nx.draw_networkx_edges(g, pos, edgelist=p2,
                           edge_color='b', width=1.5, alpha=0.7)

    p = [g.nodes[p1[0][0]]['pos']] + [g.nodes[y]['pos'] for _, y in p1]
    q = [g.nodes[p2[0][0]]['pos']] + [g.nodes[y]['pos'] for _, y in p2]
    print(frechet(p, q))

    plt.gca().set_aspect('equal')
    # plt.savefig('suurballe_disjoint_path_01.png', bbox_inches='tight')
    plt.show()
