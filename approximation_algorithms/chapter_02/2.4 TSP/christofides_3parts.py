import itertools
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc


def get_complete_graph(P):
    g = nx.Graph()
    edges = []
    for i, j in itertools.combinations(range(len(P)), 2):
        edges.append((i, j, np.linalg.norm(P[i] - P[j])))
    g.add_weighted_edges_from(edges)
    return g


def extract_odd_degree_vertices(Te):
    tg = nx.Graph()
    tg.add_edges_from(Te)
    O = []
    for v in tg.nodes():
        if tg.degree(v) % 2 != 0:
            O.append(v)
    return O


def get_perfect_matching_on_subgraph_induced_by(G, O):
    sg = G.subgraph(O)
    for u, v in sg.edges_iter():
        sg[u][v]['weight'] *= (-1)
    m = nx.max_weight_matching(sg, maxcardinality=True)
    return [[u, v] for u, v in m.iteritems() if u < v]

def draw_minimum_spanning_tree(P, Te, ax):
    lines = [[P[u], P[v]] for u, v in Te]
    lc = mc.LineCollection(lines, colors='y', lw=1.5, zorder=-1)
    ax.add_collection(lc)


def get_christofides_tour(P):
    G = get_complete_graph(P)

    Te = [(u, v) for u, v, w in nx.minimum_spanning_edges(G)]

    O = extract_odd_degree_vertices(Te)

    pm = get_perfect_matching_on_subgraph_induced_by(G, O)

    eg = nx.MultiGraph()
    eg.add_edges_from(Te + pm)

    checked = [False] * len(P)
    christofides_tour = []
    for u, v in nx.eulerian_circuit(eg):
        if not checked[u]:
            christofides_tour.append(u)
            checked[u] = True
    christofides_tour.append(christofides_tour[0])
    return (Te, O, pm, christofides_tour)



def draw_tours(P):
    Te, O, pm, c_tour = get_christofides_tour(P)
    f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(9, 4))

    o = np.array([P[i] for i in O])

    ax1.scatter([P[0][0]], [P[0][1]], color='r', s=30)
    ax1.scatter(P[:, 0], P[:, 1], color='r', s=8)
    ax1.scatter(o[:, 0], o[:, 1], color='y', alpha=0.8, s=20, zorder=3)

    ax2.scatter(P[:, 0], P[:, 1], color='r', s=8)
    ax2.scatter(o[:, 0], o[:, 1], color='g', alpha=0.5, s=20, zorder=3)

    ax3.scatter(P[:, 0], P[:, 1], color='r', s=8)

    draw_minimum_spanning_tree(P, Te, ax1)

    lines = [[P[u], P[v]] for u, v in pm]
    lc = mc.LineCollection(lines, colors='b', alpha=0.5, lw=1.5, zorder=0)
    ax2.add_collection(lc)


    lines = [[P[u], P[v]] for u, v in zip(c_tour[:-1], c_tour[1:])]
    lc = mc.LineCollection(lines, colors='g', linewidth=2, zorder=-4)
    ax3.add_collection(lc)

    ax1.set_aspect('equal')
    ax2.set_aspect('equal')
    ax3.set_aspect('equal')
    plt.tight_layout()


if __name__ == '__main__':
    n = 25
    np.random.seed(2)
    P = np.random.random((n, 2))
    draw_tours(P)
    plt.savefig('3parts_on_christofes_tour.png', bbox_inches='tight')
    plt.show()
