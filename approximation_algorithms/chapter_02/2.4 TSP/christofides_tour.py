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
    return christofides_tour


def draw_tours(P):
    plt.gca().scatter(P[:, 0], P[:, 1], color='r', s=8)

    c_tour = get_christofides_tour(P)

    lines = [[P[u], P[v]] for u, v in zip(c_tour[:-1], c_tour[1:])]
    lc = mc.LineCollection(lines, colors='g', linewidth=2, zorder=-1)
    plt.gca().add_collection(lc)

    plt.gca().autoscale()
    plt.gca().set_aspect('equal')


if __name__ == '__main__':
    np.random.seed(1)
    P = np.random.random((50, 2))
    draw_tours(P)
    plt.show()
