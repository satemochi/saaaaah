import itertools
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc


def gen2(n=3):
    np.random.seed(6)
    ang = (30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
#
#    np.random.seed(5)
#    ang = (30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160,
#           170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290,
#           300, 310, 320, 330)

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


def get_double_tree_tour(n, Te):
    Eulerian_Graph = nx.MultiGraph()
    Eulerian_Graph.add_edges_from(Te + Te)
    checked = [False] * n
    double_tree_tour = []
    for u, v in nx.eulerian_circuit(Eulerian_Graph):
        if not checked[u]:
            double_tree_tour.append(u)
            checked[u] = True
    double_tree_tour.append(double_tree_tour[0])
    return double_tree_tour


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


def get_christofides_tour(G, n, Te):
    O = extract_odd_degree_vertices(Te)
    pm = get_perfect_matching_on_subgraph_induced_by(G, O)
    eg = nx.MultiGraph()
    eg.add_edges_from(Te + pm)
    checked = [False] * n
    christofides_tour = []
    for u, v in nx.nx.eulerian_circuit(eg):
        if not checked[u]:
            christofides_tour.append(u)
            checked[u] = True
    christofides_tour.append(christofides_tour[0])
    return christofides_tour


def draw_tour(ax, P, tour, title="a: "):
    ax.scatter(P[:, 0], P[:, 1], color='r', s=8)
    lines = [[P[u], P[v]] for u, v in zip(tour[:-1], tour[1:])]
    ax.add_collection(mc.LineCollection(lines, colors='g',
                                               linewidth=2, zorder=-1))
    tour_length = 0.0
    for s, t in lines:
        tour_length += np.linalg.norm(s - t)
    ax.set_title(title + str(tour_length), fontsize=10)
    ax.set_aspect('equal')
    ax.autoscale()


def draw_tours(P):
    G = get_complete_graph(P)
    Te = [(u, v) for u, v, w in nx.minimum_spanning_edges(G)]

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 4))

    d_tour = get_double_tree_tour(len(P), Te)
    c_tour = get_christofides_tour(G, len(P), Te)

    draw_tour(ax1, P, d_tour, "Double tree: ")
    draw_tour(ax2, P, c_tour, "Christofides': ")


if __name__ == '__main__':
    P = gen2()
    draw_tours(P)
    plt.savefig('comp_dc_tours.png', bbox_inches='tight')
    plt.show()
