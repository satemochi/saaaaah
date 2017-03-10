import itertools
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc


def gen(n=2, k=3):
    P = np.random.random((n, 2)) + np.random.randint(0, 10, 2)
    for i in range(k-1):
        pts = np.random.random((n, 2)) + np.random.randint(0, 10, 2)
        P = np.concatenate((P, pts))
    return P

def gen2(n=2):
    np.random.seed(1)
    ang = (30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
    radius = 10
    x = np.cos(np.array(ang) * np.pi / 180.) * radius
    y = np.sin(np.array(ang) * np.pi / 180.) * radius
    P = np.random.random((n, 2)) + np.array([x[0], y[0]])
    for i in range(1, len(ang)):
        pts = np.random.random((n, 2)) + np.array([x[i], y[i]])
        P = np.concatenate((P, pts))
    return P

def get_complete_graph(P):
    g = nx.Graph()
    edges = []
    for i, j in itertools.combinations(range(len(P)), 2):
        edges.append((i, j, np.linalg.norm(P[i] - P[j])))
    g.add_weighted_edges_from(edges)
    return g


def draw_minimum_spanning_tree(P, Te):
    lines = []
    for u, v in Te:
        lines.append([P[u], P[v]])
    lc = mc.LineCollection(lines, colors='y', lw=1, zorder=-1)
    plt.gca().add_collection(lc)


def get_double_tree_tour(n, Te):
    checked = [False] * n
    tour = []
    g = nx.MultiGraph()
    g.add_edges_from(Te + Te)
    for u, v in nx.eulerian_circuit(g):
        if not checked[u]:
            tour.append(u)
            checked[u] = True
    tour.append(tour[0])
    return tour


def draw_tour(P):
    plt.gca().scatter(P[:, 0], P[:, 1], color='r', s=5)

    G = get_complete_graph(P)
    Te = [(u, v) for u, v, w in nx.minimum_spanning_edges(G)]
    draw_minimum_spanning_tree(P, Te)

    d_tour = get_double_tree_tour(len(P), Te)

    lines = [[P[u], P[v]] for u, v in zip(d_tour[:-1], d_tour[1:])]
    lc = mc.LineCollection(lines, colors='g', linewidth=2, zorder=-3)
    plt.gca().add_collection(lc)
    plt.autoscale()
    plt.gca().set_aspect('equal')


if __name__ == '__main__':
    n, k = 10, 4
#    P = gen(n, k * 1)
    P = gen2(3)
    draw_tour(P)
    plt.show()
